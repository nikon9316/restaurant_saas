from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Order, User, Product, Category, Restaurant, OrderItem
from app.bot.notifications import notify_user_status

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/orders/{restaurant_id}")
async def get_orders(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(select(Order).where(Order.restaurant_id == restaurant_id).order_by(Order.created_at.desc()))
    orders = rows.all()
    result = []
    for order in orders:
        user = await db.get(User, order.user_id)
        items = await db.scalars(select(OrderItem).where(OrderItem.order_id == order.id))
        result.append({
            "id": order.id,
            "order_number": order.order_number,
            "client_name": user.name if user else "-",
            "phone": user.phone if user else "-",
            "total_sum": order.total_sum,
            "delivery_type": order.delivery_type,
            "payment_method": order.payment_method,
            "address": order.address,
            "comment": order.comment,
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [{"name": i.product_name, "qty": i.quantity, "total": i.total} for i in items.all()]
        })
    return result

@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: int, payload: dict, request: Request, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    order.status = payload["status"]
    await db.commit()
    user = await db.get(User, order.user_id)
    if user:
        await notify_user_status(request.app.state.bot, user.telegram_id, order.order_number, order.status)
    return {"ok": True}

@router.get("/products/{restaurant_id}")
async def admin_products(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(select(Product).where(Product.restaurant_id == restaurant_id))
    return rows.all()

@router.post("/products")
async def create_product(payload: dict, db: AsyncSession = Depends(get_db)):
    p = Product(**payload)
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return p

@router.patch("/products/{product_id}")
async def update_product(product_id: int, payload: dict, db: AsyncSession = Depends(get_db)):
    p = await db.get(Product, product_id)
    if not p:
        raise HTTPException(404, "Product not found")
    for k, v in payload.items():
        if hasattr(p, k):
            setattr(p, k, v)
    await db.commit()
    return {"ok": True}

@router.get("/categories/{restaurant_id}")
async def admin_categories(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(select(Category).where(Category.restaurant_id == restaurant_id).order_by(Category.sort_order))
    return rows.all()

@router.post("/categories")
async def create_category(payload: dict, db: AsyncSession = Depends(get_db)):
    c = Category(**payload)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c

@router.get("/clients/{restaurant_id}")
async def clients(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.execute(
        select(User, Order).join(Order, Order.user_id == User.id).where(Order.restaurant_id == restaurant_id)
    )
    data = {}
    for user, order in rows.all():
        if user.id not in data:
            data[user.id] = {"name": user.name, "phone": user.phone, "telegram_id": user.telegram_id, "orders": 0, "spent": 0}
        data[user.id]["orders"] += 1
        data[user.id]["spent"] += order.total_sum
    return list(data.values())

@router.patch("/settings/{restaurant_id}")
async def update_settings(restaurant_id: int, payload: dict, db: AsyncSession = Depends(get_db)):
    r = await db.get(Restaurant, restaurant_id)
    if not r:
        raise HTTPException(404, "Restaurant not found")
    for k, v in payload.items():
        if hasattr(r, k):
            setattr(r, k, v)
    await db.commit()
    return {"ok": True}
