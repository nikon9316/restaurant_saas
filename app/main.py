import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.config import BOT_TOKEN, WEB_HOST, WEB_PORT
from app.database import init_db
from app.bot.handlers import router as bot_router
from app.api.client_routes import router as client_router
from app.api.admin_routes import router as admin_router
import os

app = FastAPI(title="Restaurant SaaS MVP")
app.include_router(client_router)
app.include_router(admin_router)
os.makedirs("app/static/uploads", exist_ok=True)
app.mount("/webapp", StaticFiles(directory="app/static/webapp", html=True), name="webapp")
app.mount("/admin", StaticFiles(directory="app/static/admin", html=True), name="admin")
app.mount("/uploads", StaticFiles(directory="app/static/uploads"), name="uploads")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(bot_router)
app.state.bot = bot

async def start_api():
    config = uvicorn.Config(app, host=WEB_HOST, port=WEB_PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def start_bot():
    await dp.start_polling(bot)

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty. Fill .env")
    await init_db()
    await asyncio.gather(start_api(), start_bot())

if __name__ == "__main__":
    asyncio.run(main())
