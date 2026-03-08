"""SQLite-based persona storage."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

_DEFAULT_DB = Path("memory/personas.db")


class PersonaStore:
    def __init__(self, db_path: Path = _DEFAULT_DB):
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path))
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS personas (
                bot_name    TEXT PRIMARY KEY,
                persona     TEXT NOT NULL,
                created_by  TEXT DEFAULT '',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def get(self, bot_name: str) -> Optional[str]:
        row = self._conn.execute(
            "SELECT persona FROM personas WHERE bot_name = ?", (bot_name,)
        ).fetchone()
        return row["persona"] if row else None

    def set(self, bot_name: str, persona: str, created_by: str = "") -> None:
        now = datetime.now(timezone.utc).isoformat()
        self._conn.execute("""
            INSERT INTO personas (bot_name, persona, created_by, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(bot_name) DO UPDATE SET
                persona = excluded.persona,
                updated_at = excluded.updated_at
        """, (bot_name, persona, created_by, now, now))
        self._conn.commit()

    def delete(self, bot_name: str) -> bool:
        cur = self._conn.execute(
            "DELETE FROM personas WHERE bot_name = ?", (bot_name,)
        )
        self._conn.commit()
        return cur.rowcount > 0

    def list_all(self) -> List[Dict]:
        rows = self._conn.execute(
            "SELECT * FROM personas ORDER BY bot_name"
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self):
        self._conn.close()
