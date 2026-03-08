"""Shim — TeamLeadBot is now BaseMarketingBot with dynamic persona."""

from src.adapters.discord.base_bot import BaseMarketingBot as TeamLeadBot

__all__ = ["TeamLeadBot"]
