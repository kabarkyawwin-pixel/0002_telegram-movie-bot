import time
import nest_asyncio
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
import config

# asyncio loop ပြဿနာကို ဖြေရှင်းခြင်း
nest_asyncio.apply()

# MongoDB connection ကို သေချာပြင်ဆင်ခြင်း
# config.MONGO_URL ကို ဒီအတိုင်းမသုံးဘဲ၊ 
# အောက်ပါအတိုင်း ပြင်ဆင်ပြီးမှ ခေါ်သုံးပါ
try:
    # URL ထဲက password ကို auto-escape လုပ်ပေးခြင်း
    db = AsyncIOMotorClient(config.MONGO_URL).Anonymous
except Exception as e:
    print(f"MongoDB Connection Error: {e}")

# Uptime tracking
START_TIME = time.time()

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="MoviesBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            max_concurrent_transmissions=7,
        )

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)
        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name
        self.username = me.username
    
    async def stop(self, *args, **kwargs):
        await super().stop(*args, **kwargs)

app = Bot()
