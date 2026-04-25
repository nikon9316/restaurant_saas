from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from app.config import WEBAPP_URL, ADMIN_WEBAPP_URL

def main_menu(restaurant_id: int = 1) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍽 Открыть меню", web_app=WebAppInfo(url=f"{WEBAPP_URL}?restaurant_id={restaurant_id}"))],
        [InlineKeyboardButton(text="🛠 Админка", web_app=WebAppInfo(url=f"{ADMIN_WEBAPP_URL}?restaurant_id={restaurant_id}"))],
    ])
