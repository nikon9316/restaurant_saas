import os
from dotenv import load_dotenv

load_dotenv()

# --- Telegram ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# --- Base URL (ОБЯЗАТЕЛЬНО с https) ---
BASE_PUBLIC_URL = os.getenv(
    "BASE_PUBLIC_URL",
    "https://restaurantsaas-production.up.railway.app"
).rstrip("/")

# --- Database ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./restaurant_saas.db"
)

# --- Server (ВАЖНО для Railway) ---
WEB_HOST = "0.0.0.0"
WEB_PORT = int(os.getenv("PORT", "8080"))

# --- WebApp URLs ---
WEBAPP_URL = os.getenv(
    "WEBAPP_URL",
    f"{BASE_PUBLIC_URL}/webapp/index.html"
)

ADMIN_WEBAPP_URL = os.getenv(
    "ADMIN_WEBAPP_URL",
    f"{BASE_PUBLIC_URL}/admin/index.html"
)
