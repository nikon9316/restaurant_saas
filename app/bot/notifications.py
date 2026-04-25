from aiogram import Bot
from app.services.order_service import STATUS_TEXT

async def notify_user_status(bot: Bot, telegram_id: int, order_number: int, status: str):
    text = STATUS_TEXT.get(status, "Статус заказа обновлен.")
    await bot.send_message(telegram_id, f"{text}\n\nЗаказ №{order_number}")

async def notify_admins_new_order(bot: Bot, admin_ids: list[int], order):
    text = (
        f"🆕 Новый заказ №{order.order_number}\n"
        f"Сумма: {order.total_sum:,.0f} сум\n"
        f"Получение: {order.delivery_type}\n"
        f"Оплата: {order.payment_method}\n"
        f"Адрес: {order.address or '-'}\n"
        f"Комментарий: {order.comment or '-'}"
    )
    for admin_id in admin_ids:
        await bot.send_message(admin_id, text)
