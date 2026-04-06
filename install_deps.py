import subprocess
import sys

packages = [
    'fake-useragent>=1.4.0',
    'selenium>=4.15.0',
    'requests>=2.31.0',
    'colorama>=0.4.6',
    'python-dotenv>=1.0.0',
    'loguru>=0.7.2',
    'webdriver-manager>=4.0.1',
    'pydantic>=2.0.0',
    'sqlalchemy>=2.0.0',
    'flask>=3.0.0',
    'flask-cors>=4.0.0',
    'aiohttp>=3.9.0',
    'psutil>=5.9.0',
]

print("📦 Установка всех зависимостей...\n")

for package in packages:
    pkg_name = package.split('>=')[0].split('==')[0]
    print(f"📥 Устанавливаю {pkg_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        print(f"✅ {pkg_name} - установлен\n")
    except Exception as e:
        print(f"⚠️  Ошибка: {e}\n")

print("✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ!")