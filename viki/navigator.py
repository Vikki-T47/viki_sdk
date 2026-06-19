import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VikiNavigator:
    """Durable Memory & Black Box Tracer."""
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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_trace (
                    task_id TEXT,
                    step_index INTEGER,
                    timestamp TEXT,
                    reasoning TEXT,
                    delta TEXT
                )
            """)

    def save_checkpoint(self, task_id, step_index, total_steps, state_data, status="ACTIVE"):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO chain_states 
                (task_id, current_step, total_steps, state_data, status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task_id, step_index, total_steps, json.dumps(state_data), status, datetime.now()))

    def log_trace(self, task_id, step, reasoning, delta):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO audit_trace (task_id, step_index, timestamp, reasoning, delta)
                VALUES (?, ?, ?, ?, ?)
            """, (task_id, step, datetime.now().isoformat(), reasoning, delta))

    def load_state(self, task_id):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT current_step, total_steps, state_data, status FROM chain_states WHERE task_id = ?", (task_id,)).fetchone()
            if row:
                return {"current_step": row[0], "total_steps": row[1], "state_data": json.loads(row[2]), "status": row[3]}
        return None

    def replay(self, task_id):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT step_index, reasoning, delta FROM audit_trace WHERE task_id=? ORDER BY step_index", (task_id,)).fetchall()
            return rows