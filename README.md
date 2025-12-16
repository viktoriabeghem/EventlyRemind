# EventlyRemind
Командний проєкт: бот на Python, який зберігає події в Django-базу даних. Адмінка для керування подіями.

## Запуск локально
1. Клонувати репозиторій
```
git clone <url>
```
---
2. Встановити залежності:
```
pip install -r requirements.txt
```
---
3.Виконати міграції:
```
python manage.py makemigrations
python manage.py migrate
```
---

4.Створити суперкористувача:
```
python manage.py createsuperuser
```
---
5.Запустити сервер:
```
python manage.py runserver

```


## 6.. API ендпоінти
```markdown
## API ендпоінти
- `GET /api/events/` — список подій
- `POST /api/events/create/` — створення події
- `GET /api/events/<id>/` — деталі події
- `PATCH /api/events/<id>/update/` — оновлення події
- `DELETE /api/events/<id>/delete/` — видалення події

---
```

## 7.. Приклад запиту на створення події
```
Створення події (POST /api/events/create/)
Формат: multipart/form-data

Поля:
- user_id (integer, обов’язкове)
- date (YYYY-MM-DD)
- time (HH:MM)
- location (string)
- link (URL)
- is_sent (boolean)
- added_to_calendar (boolean)
- photo (file, необов’язкове)

Приклад відповіді:
```json
{
  "id": 7,
  "photo": "/media/event_photos/username.png",
  "date": "2025-12-16",
  "time": "13:00",
  "location": "офіс",
  "link": "https://meet.google.com/xyz",
  "is_sent": false,
  "added_to_calendar": false
}

---
```

## 8.. Медіа
```markdown
## Медіа
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`
- Доступ до файлів: `http://127.0.0.1:8000/media/event_photos/<filename>`

## CORS
- Для локальної розробки: `CORS_ALLOW_ALL_ORIGINS = True`
- Для продакшн: вказати конкретні дозволені origins у `CORS_ALLOWED_ORIGINS`
