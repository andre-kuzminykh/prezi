"""Entry point for the Telegram bot.

## Traceability
Component: Bot Application Entry Point
"""
import asyncio
import logging

from core.loader import bot, dp
from handler.include_router import setup_routers


async def main():
    """Start the bot with polling."""
    logging.basicConfig(level=logging.INFO)
    setup_routers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
