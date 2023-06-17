import asyncio

from aiogram import Bot, Dispatcher
import nats
from aiogram.types import Message
from aiogram import F
from nats.js.object_store import ObjectStore

bot = Bot("token")
dp = Dispatcher()


@dp.message(F.photo)
async def photo(m: Message):
    nats_conn = await nats.connect(['nats://localhost:4222'])
    js = nats_conn.jetstream()
    # await js.create_object_store("nyam")
    a = await js.object_store("nyam")
    await a.put(
        name = f"photo_id_from_{m.from_user.id}",
        data = m.photo[-1].file_id.encode(),
    )
    qwe = ObjectStore.ObjectResult(await a.get(f"photo_id_from_{m.from_user.id}"))
    print(qwe.info.bucket)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
