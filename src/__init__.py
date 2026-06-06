import time
import nest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import config

# asyncio loop ကို အရင်ပြင်ပေးမယ်
nest_asyncio.apply()

# MongoDB connection
db = AsyncIOMotorClient(config.MONGO_URL).Anonymous
START_TIME = time.time()

# ဒီနေရာမှာ Client ကို Import မလုပ်ပါနဲ့
from pyrogram import Client 

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

# ဒီ app ကို __main__.py ကနေမှ ခေါ်သုံးမှာပါ
app = Bot()
