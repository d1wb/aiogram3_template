from aiogram import types, Router

echo_router = Router()


@echo_router.message()
async def echo(message: types.Message):
    await message.answer('Такой команды не существует')
