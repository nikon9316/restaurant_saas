# Restaurant SaaS Telegram WebApp MVP

## Запуск локально

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python -m app.seed
python -m app.main
```

Открыть:
- WebApp: http://127.0.0.1:8000/webapp/index.html?restaurant_id=1
- Admin: http://127.0.0.1:8000/admin/admin.html?restaurant_id=1

## Важно
В .env вставь BOT_TOKEN и свой ADMIN_ID.
