from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.bot.keyboards import main_menu

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    restaurant_id = 1
    args = message.text.split(maxsplit=1)
    if len(args) > 1 and args[1].startswith("restaurant_"):
        try:
            restaurant_id = int(args[1].replace("restaurant_", ""))
        except ValueError:
            restaurant_id = 1

    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=main_menu(restaurant_id)
    )
