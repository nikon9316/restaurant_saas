import asyncio
from sqlalchemy import select
from app.database import init_db, AsyncSessionLocal
from app.models import Restaurant, Category, Product, Admin
from app.config import ADMIN_ID

async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        exists = await db.scalar(select(Restaurant).where(Restaurant.id == 1))
        if exists:
            print("Seed already exists")
            return
        r = Restaurant(
            id=1,
            name="Demo Cafe",
            logo_url="",
            brand_color="#111827",
            phone="+998 90 000 00 00",
            address="Самарканд",
            delivery_price=15000,
            min_order_sum=50000,
        )
        db.add(r)
        await db.flush()
        pizza = Category(restaurant_id=1, name="🍕 Пицца", sort_order=1)
        drinks = Category(restaurant_id=1, name="🥤 Напитки", sort_order=2)
        db.add_all([pizza, drinks])
        await db.flush()
        db.add_all([
            Product(restaurant_id=1, category_id=pizza.id, name="Пепперони", description="Пицца с колбасой пепперони", price=75000, image_url=""),
            Product(restaurant_id=1, category_id=pizza.id, name="Маргарита", description="Сыр, томаты, соус", price=65000, image_url=""),
            Product(restaurant_id=1, category_id=drinks.id, name="Coca-Cola 1L", description="Холодный напиток", price=12000, image_url=""),
        ])
        if ADMIN_ID:
            db.add(Admin(restaurant_id=1, telegram_id=ADMIN_ID, role="owner"))
        await db.commit()
        print("Seed completed")

if __name__ == "__main__":
    asyncio.run(seed())
