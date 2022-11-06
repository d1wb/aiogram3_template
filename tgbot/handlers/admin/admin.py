from aiogram import types, Router

from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message()
async def admin_handler(message: types.Message):
    await message.answer('Привет админ')
