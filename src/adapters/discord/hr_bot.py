"""Shim — HRBot is now BaseMarketingBot with dynamic persona.

Re-exports domain HR functions for backward compatibility.
"""

from src.adapters.discord.base_bot import BaseMarketingBot as HRBot
from src.domain.hr import (
    BOT_NAME_ALIASES,
    HISTORY_FIRE_THRESHOLD,
    HISTORY_WARN_THRESHOLD,
    PROTECTED_KEYS,
    fire_bot,
    hire_bot,
    resolve_bot,
    status_report,
)

__all__ = [
    "BOT_NAME_ALIASES",
    "PROTECTED_KEYS",
    "HISTORY_WARN_THRESHOLD",
    "HISTORY_FIRE_THRESHOLD",
    "resolve_bot",
    "fire_bot",
    "hire_bot",
    "status_report",
    "HRBot",
]
