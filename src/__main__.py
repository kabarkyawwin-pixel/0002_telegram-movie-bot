import asyncio
import importlib
from pyrogram import idle, errors
from pyrogram.enums import ChatMemberStatus
from src import app, config
from src.modules import ALL_MODULES
from src.logging import LOGGER

async def main():
    LOGGER(__name__).info("Bot is starting...")
    
    try:
        await app.start()
        LOGGER(__name__).info("Bot started successfully.")
    except Exception as e:
        LOGGER(__name__).error(f"Failed to start bot: {e}")
        return

    try:
        await app.send_message(
            chat_id=config.LOGGER_ID,
            text="<u><b>» Bot Started.</b></u>"
        )
    except Exception as e:
        LOGGER(__name__).error(f"Failed to send log message: {e}")

    for module in ALL_MODULES:
        importlib.import_module(f"src.modules.{module}")
    
    LOGGER(__name__).info("All modules loaded successfully.")

    await idle()
    
    LOGGER(__name__).warning("Bot is shutting down...")
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER(__name__).warning("Bot interrupted.")
