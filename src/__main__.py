import asyncio
import importlib

from pyrogram import idle, errors
from pyrogram.enums import ChatMemberStatus

from src import app, config
from src.modules import ALL_MODULES
from src.logging import LOGGER

async def boot():
    LOGGER(__name__).info("Bot is starting...")
    
    # ပိုနေတဲ့ စာကြောင်းတွေကို ဖျက်ပြီး တစ်ကြိမ်ပဲ ထားထားပါတယ်
    await asyncio.sleep(2)
    await app.start()
    LOGGER(__name__).info("Bot started successfully.")

    try:
        await app.send_message(
            chat_id=config.LOGGER_ID,
            text="<u><b>» Bot Started.</b></u>"
        )
    except (errors.ChannelInvalid, errors.PeerIdInvalid):
        LOGGER(__name__).error("Bot can't access log group.")
        return
    except Exception as ex:
        LOGGER(__name__).error(f"Failed to send log message: {type(ex).__name__}")
        return

    try:
        member = await app.get_chat_member(config.LOGGER_ID, app.id)
        if member.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error("Bot is not admin in log group.")
            return
    except Exception as ex:
        LOGGER(__name__).error(f"Failed to check admin status: {type(ex).__name__}")
        return

    for module in ALL_MODULES:
        importlib.import_module(f"src.modules.{module}")
    
    LOGGER(__name__).info("All modules loaded successfully.")

    try:
        await idle()
    finally:
        LOGGER(__name__).warning("Bot is shutting down...")
        await app.stop()

if __name__ == "__main__":
    try:
        # asyncio.run ကို သုံးခြင်းက Python 3.10+ အတွက် ပိုပြီးတည်ငြိမ်ပါတယ်
        asyncio.run(boot())
    except KeyboardInterrupt:
        LOGGER(__name__).warning("Bot interrupted by user or system.")
    except Exception as e:
        LOGGER(__name__).error(f"Bot failed to start: {e}")
