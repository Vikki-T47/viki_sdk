import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VikiNavigator:
    """Черный ящик и система чекпоинтов. Обеспечивает выносливость и аудит."""
    def __init__(self, db_path="viki_state.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            # Таблица состояний
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chain_states (
                    task_id TEXT PRIMARY KEY,
                    current_step INTEGER,
                    state_data TEXT,
                    status TEXT,
                    updated_at TIMESTAMP
                )
            """)
            # Таблица трассировки (Black Box)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_trace (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT,
                    step_index INTEGER,
                    raw_prompt TEXT,
                    reasoning TEXT,
                    tool_call TEXT,
                    dvp_delta TEXT,
                    timestamp TIMESTAMP
                )
            """)

    def save_checkpoint(self, task_id, step_index, state_data, status="ACTIVE"):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO chain_states 
                (task_id, current_step, state_data, status, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (task_id, step_index, json.dumps(state_data), status, datetime.now()))

    def log_trace(self, task_id, step_index, prompt, reasoning, tool_call, delta):
        """Запись в Black Box для функции Replay."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO audit_trace (task_id, step_index, raw_prompt, reasoning, tool_call, dvp_delta, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task_id, step_index, prompt, reasoning, json.dumps(tool_call), str(delta), datetime.now()))
        logger.info(f"💾 [BLACK_BOX] Trace recorded for Task {task_id}, Step {step_index}")

    def replay(self, task_id):
        """Воспроизведение пути рассуждений."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT step_index, reasoning, dvp_delta FROM audit_trace WHERE task_id = ? ORDER BY step_index", (task_id,)).fetchall()
            return rows