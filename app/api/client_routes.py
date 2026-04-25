from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Restaurant, Category, Product, Order, User
from app.services.order_service import create_order, get_restaurant_admin_ids
from app.bot.notifications import notify_admins_new_order

router = APIRouter(prefix="/api", tags=["client"])

@router.get("/restaurant/{restaurant_id}")
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.get(Restaurant, restaurant_id)
    return r

@router.get("/categories/{restaurant_id}")
async def get_categories(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(
        select(Category).where(Category.restaurant_id == restaurant_id, Category.is_active == True).order_by(Category.sort_order)
    )
    return rows.all()

@router.get("/products/{restaurant_id}")
async def get_products(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(
        select(Product).where(Product.restaurant_id == restaurant_id, Product.is_active == True)
    )
    return rows.all()

@router.post("/orders")
async def post_order(payload: dict, request: Request, db: AsyncSession = Depends(get_db)):
    order = await create_order(db, payload)
    bot = request.app.state.bot
    admin_ids = await get_restaurant_admin_ids(db, order.restaurant_id)
    await notify_admins_new_order(bot, admin_ids, order)
    return {"ok": True, "order_id": order.id, "order_number": order.order_number, "total_sum": order.total_sum}

@router.get("/orders/user/{telegram_id}")
async def get_user_orders(telegram_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.telegram_id == telegram_id))
    if not user:
        return []
    rows = await db.scalars(select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc()))
    return rows.all()
