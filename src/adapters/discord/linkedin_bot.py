"""Shim — LinkedInBot is now BaseMarketingBot with dynamic persona."""

from src.adapters.discord.base_bot import BaseMarketingBot as LinkedInBot

__all__ = ["LinkedInBot"]
