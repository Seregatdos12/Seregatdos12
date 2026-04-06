import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ПУТИ
BASE_DIR = Path(__file__).parent
STORAGE_DIR = BASE_DIR / "storage"
LOG_DIR = STORAGE_DIR / "logs"
COOKIES_DIR = STORAGE_DIR / "cookies"
SESSIONS_DIR = STORAGE_DIR / "sessions"
REPORTS_DIR = STORAGE_DIR / "reports"

# Создание директорий
for d in [LOG_DIR, COOKIES_DIR, SESSIONS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# КОНФИГУРАЦИЯ АККАУНТОВ
ACCOUNTS = {
    "account_1": {
        "id": "account_1",
        "name": "🏍️ Мото Аккаунт #1",
        "login": os.getenv("LOGIN_1", "email1@mail.ru"),
        "password": os.getenv("PASS_1", "password1"),
    },
    "account_2": {
        "id": "account_2",
        "name": "🏍️ Мото Аккаунт #2",
        "login": os.getenv("LOGIN_2", "email2@mail.ru"),
        "password": os.getenv("PASS_2", "password2"),
    },
    "account_3": {
        "id": "account_3",
        "name": "🏍️ Мото Аккаунт #3",
        "login": os.getenv("LOGIN_3", "email3@mail.ru"),
        "password": os.getenv("PASS_3", "password3"),
    },
    "account_4": {
        "id": "account_4",
        "name": "🏍️ Мото Аккаунт #4",
        "login": os.getenv("LOGIN_4", "email4@mail.ru"),
        "password": os.getenv("PASS_4", "password4"),
    },
    "account_5": {
        "id": "account_5",
        "name": "🏍️ Мото Аккаунт #5",
        "login": os.getenv("LOGIN_5", "email5@mail.ru"),
        "password": os.getenv("PASS_5", "password5"),
    },
}

# ПАРАМЕТРЫ ПРОГРЕВА
WARMUP_CONFIG = {
    'total_duration': 95,  # минут
    'phase_1_duration': 15,  # Прогрев браузера
    'phase_2_duration': 20,  # Изучение Юлы
    'phase_3_duration': 15,  # Настройка профиля
    'phase_4_duration': 25,  # Просмотр объявлений
    'headless_mode': False,
    'use_proxy': False,
}

# ЛОГИРОВАНИЕ
LOG_CONFIG = {
    'level': os.getenv("LOG_LEVEL", "INFO"),
    'format': "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    'rotation': "500 MB",
}

# FLASK
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"