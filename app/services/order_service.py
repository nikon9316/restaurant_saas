from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Product, Order, OrderItem, Admin

STATUS_TEXT = {
    "new": "✅ Ваш заказ принят.",
    "accepted": "✅ Заказ принят рестораном.",
    "cooking": "👨‍🍳 Заказ готовится.",
    "ready": "🍽 Заказ готов.",
    "delivery": "🚗 Заказ уже в пути.",
    "done": "✅ Заказ доставлен. Приятного аппетита!",
    "cancelled": "❌ Заказ отменен.",
}

async def create_order(db: AsyncSession, data: dict) -> Order:
    tg_id = int(data["telegram_id"])
    user = await db.scalar(select(User).where(User.telegram_id == tg_id))
    if not user:
        user = User(telegram_id=tg_id, name=data.get("name"), phone=data.get("phone"))
        db.add(user)
        await db.flush()
    else:
        user.name = data.get("name") or user.name
        user.phone = data.get("phone") or user.phone

    total = 0.0
    order_items = []
    for item in data.get("items", []):
        product = await db.get(Product, int(item["product_id"]))
        if not product or not product.is_active:
            continue
        qty = int(item.get("quantity", 1))
        line_total = product.price * qty
        total += line_total
        order_items.append(OrderItem(
            product_id=product.id,
            product_name=product.name,
            quantity=qty,
            price=product.price,
            total=line_total,
        ))

    last_number = await db.scalar(select(func.max(Order.order_number)).where(Order.restaurant_id == data["restaurant_id"]))
    order = Order(
        restaurant_id=int(data["restaurant_id"]),
        user_id=user.id,
        order_number=(last_number or 1000) + 1,
        total_sum=total,
        delivery_type=data.get("delivery_type", "delivery"),
        payment_method=data.get("payment_method", "cash"),
        address=data.get("address"),
        comment=data.get("comment"),
        status="new",
        items=order_items,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def get_restaurant_admin_ids(db: AsyncSession, restaurant_id: int) -> list[int]:
    rows = await db.scalars(select(Admin.telegram_id).where(Admin.restaurant_id == restaurant_id))
    return list(rows.all())
