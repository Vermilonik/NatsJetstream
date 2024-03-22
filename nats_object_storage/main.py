import asyncio

from aiogram import Bot, Dispatcher
import nats
from aiogram.types import Message
from aiogram import F

bot = Bot("token")
dp = Dispatcher()


@dp.message(F.photo)
async def photo(m: Message):
    nats_conn = await nats.connect(['nats://localhost:4222'])
    js = nats_conn.jetstream()
    # await js.create_object_store("object_storage_kv")
    storage = await js.object_store("object_storage_kv")
    await storage.put(
        name = f"photo_id_from_{m.from_user.id}",
        data = m.photo[-1].file_id.encode(),
    )
    await m.answer(await storage.get(f"photo_id_from_{m.from_user.id}"))
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
