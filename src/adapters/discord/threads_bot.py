"""Shim — ThreadsBot is now BaseMarketingBot with dynamic persona."""

from src.adapters.discord.base_bot import BaseMarketingBot as ThreadsBot

__all__ = ["ThreadsBot"]
