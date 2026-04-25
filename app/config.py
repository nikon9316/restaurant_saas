import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
BASE_PUBLIC_URL = os.getenv("BASE_PUBLIC_URL", "http://127.0.0.1:8000").rstrip("/")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./restaurant_saas.db")
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "8000"))

WEBAPP_URL = f"{BASE_PUBLIC_URL}/webapp/index.html"
ADMIN_WEBAPP_URL = f"{BASE_PUBLIC_URL}/admin/admin.html"
