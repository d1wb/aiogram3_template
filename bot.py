import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.handlers.admin.admin import admin_router
from tgbot.handlers.echo import echo_router
from tgbot.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config()
    storage = MemoryStorage()

    bot = Bot(token=config.tg.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for admins in config.tg.admin_ids:
        await bot.send_message(admins, 'Bot started')

    for router in [
        admin_router,
        echo_router
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        logger.error('Bot stopped')
