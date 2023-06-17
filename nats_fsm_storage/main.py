import asyncio
import logging

from aiogram import Bot, Dispatcher
from Entry import NATSFSMStorage

from config_reader import config
from handlers import common, ordering_food
from nats.aio.client import Client
import nats


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    nc = await nats.connect()
    js = nc.jetstream()
    kv_states = await js.key_value('fsm_states_aiogram')
    kv_data = await js.key_value('fsm_data_aiogram')
    dp = Dispatcher(storage=NATSFSMStorage(nc, kv_states, kv_data))
    bot = Bot(config.bot_token.get_secret_value())

    dp.include_router(common.router)
    dp.include_router(ordering_food.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())