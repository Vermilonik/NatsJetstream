import asyncio
from typing import Optional

import msgpack
import nats
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram.filters.command import Command
from command_mk2 import CommandMk2
from nats.errors import TimeoutError

bot = Bot(token="5788906850:AAEd-E1dhx_XXJH2ir2zprnuA2KbYg2W130")
admin_id = 5042344467
dp = Dispatcher()


@dp.message(CommandMk2("write {num} {msg}"))
async def writer(m: types.Message, num: Optional[str], msg: Optional[str]):
    nc = await nats.connect("localhost:4222")
    js = nc.jetstream()

    for i in range(0, int(num)):
        await js.publish("mass_bullshit", msgpack.packb(msg))
        print(msg)

    await nc.close()


@dp.message(Command(commands=["listen"]))
async def listener(m: types.Message, batch_size: int = 5, polling_timeout=10):
    nc = await nats.connect("localhost:4222")
    js = nc.jetstream()
    psub = await js.pull_subscribe(subject=">", durable="aiogram")
    if not psub:
        raise ValueError("No consumer subscription, pizdec")
    while True:
        try:
            msgs = await psub.fetch(batch_size)
            for msg in msgs:
                try:
                    await bot.send_message(admin_id, msgpack.unpackb(msg.data))
                except TelegramForbiddenError:
                    pass
                await msg.ack()
        except TimeoutError:
            await m.answer("Рассылка закончена")
            break
        except TelegramRetryAfter as e:
            await asyncio.sleep(float(e.retry_after))
            continue


async def aiogram_bot():
    await asyncio.gather(dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(aiogram_bot())
