"""Tests for dynamic persona system (PersonaStore)."""

import tempfile
from pathlib import Path

from src.adapters.storage.persona_store import PersonaStore


def test_persona_store_set_and_get():
    with tempfile.TemporaryDirectory() as tmp:
        store = PersonaStore(db_path=Path(tmp) / "test.db")
        store.set("TestBot", "너는 테스트 봇임.", created_by="user#1234")
        assert store.get("TestBot") == "너는 테스트 봇임."
        store.close()


def test_persona_store_get_nonexistent():
    with tempfile.TemporaryDirectory() as tmp:
        store = PersonaStore(db_path=Path(tmp) / "test.db")
        assert store.get("NoBot") is None
        store.close()


def test_persona_store_update():
    with tempfile.TemporaryDirectory() as tmp:
        store = PersonaStore(db_path=Path(tmp) / "test.db")
        store.set("TestBot", "v1")
        store.set("TestBot", "v2")
        assert store.get("TestBot") == "v2"
        store.close()


def test_persona_store_delete():
    with tempfile.TemporaryDirectory() as tmp:
        store = PersonaStore(db_path=Path(tmp) / "test.db")
        store.set("TestBot", "persona")
        assert store.delete("TestBot") is True
        assert store.get("TestBot") is None
        store.close()


def test_persona_store_delete_nonexistent():
    with tempfile.TemporaryDirectory() as tmp:
        store = PersonaStore(db_path=Path(tmp) / "test.db")
        assert store.delete("NoBot") is False
        store.close()


def test_persona_store_list_all():
    with tempfile.TemporaryDirectory() as tmp:
        store = PersonaStore(db_path=Path(tmp) / "test.db")
        store.set("BotA", "persona A")
        store.set("BotB", "persona B")
        all_personas = store.list_all()
        assert len(all_personas) == 2
        assert all_personas[0]["bot_name"] == "BotA"
        assert all_personas[1]["bot_name"] == "BotB"
        store.close()


def test_persona_store_list_empty():
    with tempfile.TemporaryDirectory() as tmp:
        store = PersonaStore(db_path=Path(tmp) / "test.db")
        assert store.list_all() == []
        store.close()


def test_persona_store_persistence():
    """Data persists across store instances (same DB path)."""
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        store1 = PersonaStore(db_path=db_path)
        store1.set("TestBot", "persistent persona")
        store1.close()

        store2 = PersonaStore(db_path=db_path)
        assert store2.get("TestBot") == "persistent persona"
        store2.close()


def test_backward_compat_imports():
    """Empty persona constants still importable for backward compat."""
    from src.domain.persona import BOT_PERSONA
    from src.domain.personas import TEAM_LEAD_PERSONA
    assert isinstance(BOT_PERSONA, str)
    assert isinstance(TEAM_LEAD_PERSONA, str)
