import asyncio
import importlib
from aiohttp import web  # ဒါလေးကို import ထည့်ပါ (requirements.txt မှာပါရင် ရပြီ)
from pyrogram import idle, errors
from src import app, config
from src.logging import LOGGER

# Render အတွက် Port ပွင့်အောင် လုပ်ပေးခြင်း
async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    # 1. Port ဖွင့်ခြင်း (Render အတွက်)
    app_web = web.Application()
    app_web.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    LOGGER(__name__).info("Bot is starting...")
    
    try:
        await asyncio.wait_for(app.start(), timeout=30)
        LOGGER(__name__).info("Bot started successfully.")
    except Exception as e:
        LOGGER(__name__).error(f"Failed to start bot: {e}")
        return

    # ... ကျန်တဲ့ module loading တွေ ...
    
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
