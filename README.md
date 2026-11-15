# Генератор тестовых пользователей

Telegram-бот генерирует синтетические данные пользователей и отправляет результат JSON-файлом. Поддерживаются наборы из 1, 2, 5 или 10 пользователей.

Для генерации используются Faker и криптографически стойкий генератор паролей из стандартной библиотеки Python. Не используйте созданные данные как реальные контактные или учетные данные.

## Требования

- Python 3.10 или новее
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)

## Установка и запуск в Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:TELEGRAM_BOT_TOKEN = "ваш_токен_бота"
python main.py
```

Для macOS или Linux активируйте окружение командой `source .venv/bin/activate`, задайте токен командой `export TELEGRAM_BOT_TOKEN="ваш_токен_бота"` и запустите `python main.py`.

Токен хранится в переменной окружения и не должен добавляться в исходный код или публиковаться в репозитории.

## Тесты

```powershell
python -m unittest discover -s tests
```

## Структура проекта

- `main.py` — проверка конфигурации и запуск бота
- `bot.py` — Telegram-меню и обработчики сообщений
- `user_data.py` — генерация и сериализация тестовых данных
- `tests/` — автоматические тесты приложения

## Автор

[alekskobelev](https://github.com/alekskobelev)
