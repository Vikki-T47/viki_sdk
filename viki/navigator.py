import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VikiNavigator:
    """Durable Stateful Memory. Память, которая не боится перезагрузки."""
    def __init__(self, db_path="viki_state.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chain_states (
                    task_id TEXT PRIMARY KEY,
                    current_step INTEGER,
                    total_steps INTEGER,
                    state_data TEXT,
                    status TEXT,
                    updated_at TIMESTAMP
                )
            """)

    def save_checkpoint(self, task_id, step_index, total_steps, state_data, status="ACTIVE"):
        """Сохранение снимка реальности (Checkpointing)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO chain_states 
                (task_id, current_step, total_steps, state_data, status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task_id, step_index, total_steps, json.dumps(state_data), status, datetime.now()))
        logger.info(f"💾 [NAVIGATOR] Checkpoint saved: Task {task_id} at Step {step_index}")

    def load_state(self, task_id):
        """Восстановление процесса из точки падения."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM chain_states WHERE task_id = ?", (task_id,)).fetchone()
            if row:
                return {
                    "current_step": row[1],
                    "total_steps": row[2],
                    "state_data": json.loads(row[3]),
                    "status": row[4]
                }
        return None