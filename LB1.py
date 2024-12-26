# Завдання 1. [Easy] Отримання курсу валют із сайту НБУ за допомогою Postman
# 
# https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=YYYYMMDD&json
# Заміни YYYYMMDD на дату у цьому форматі

# Завдання 2. [Easy] Отримання курсу валют із сайту НБУ за допомогою Python
import requests
from datetime import datetime, timedelta

# Функція для отримання курсу валют за конкретну дату
def get_currency_rates(date: datetime):
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date.strftime('%Y%m%d')}&json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Отримання курсів за попередній тиждень
start_date = datetime.now() - timedelta(days=7)
end_date = datetime.now()

currency_rates = {}
current_date = start_date

while current_date <= end_date:
    try:
        currency_rates[current_date.strftime('%Y-%m-%d')] = get_currency_rates(current_date)
    except Exception as e:
        print(f"Failed to fetch data for {current_date.strftime('%Y-%m-%d')}: {e}")
    current_date += timedelta(days=1)

print(currency_rates)

# Завдання 3. [Easy-Medium] Побудова графіка зміни курсів валют
import matplotlib.pyplot as plt

# Візуалізація зміни курсу для USD
usd_rates = {
    date: next((rate['rate'] for rate in rates if rate['cc'] == 'USD'), None)
    for date, rates in currency_rates.items()
}

# Фільтрація даних для графіка
dates = list(usd_rates.keys())
rates = list(filter(None, usd_rates.values()))

plt.figure(figsize=(10, 5))
plt.plot(dates, rates, marker='o', linestyle='-', label='USD')
plt.xlabel('Date')
plt.ylabel('Exchange Rate (UAH)')
plt.title('USD Exchange Rate Over the Last Week')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Завдання 4. [Medium] Виконання дій із Telegram за допомогою Telethon
from telethon import TelegramClient

# Налаштування клієнта (Створений заздалегідь)
api_id = '24091219'
api_hash = '65cde1fd7678215a71b0d076a3055a7a'
client = TelegramClient('session_name', api_id, api_hash)

async def telegram_tasks():
    await client.start()

    # Отримання переліку користувачів чату/пабліку (Через посилання-запрошення, створити можна у https://my.telegram.org)
    chat_url = 'https://t.me/+W1c1EoEr-vUyZTBi'
    async for user in client.iter_participants(chat_url):
        print(f"User: {user.id}, Username: {user.username}, Name: {user.first_name} {user.last_name}")

    # Відправка повідомлення
    user_id = '+380669418450' #нік чи номер телефону
    await client.send_message(user_id, 'Hello from Python!')

    # Публікація повідомлення в чат/паблік
    await client.send_message(chat_url, 'This is a test message from Python!')

with client:
    client.loop.run_until_complete(telegram_tasks())


# Завдання 5. [Hard] Telegram Bot API - створення бота з командами menu, whisper, scream
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import Router
from aiogram import F
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n

# Налаштування токена
API_TOKEN = '8104307737:AAEhgWsEQveNkCB2NwfWK1KyyQXCjyX35uo' #API для свого бота

# Включення логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Команда /menu
@router.message(F.text == "/menu")
async def send_menu(message: Message):
    menu_text = "Available commands:\n/menu - Show this menu\n/whisper - Send a quiet message\n/scream - Send a loud message"
    await message.reply(menu_text)

# Команда /whisper
@router.message(F.text.startswith("/whisper"))
async def whisper(message: Message):
    args = message.text[len("/whisper "):].strip()
    if args:
        await message.reply(f"(whispering): {args.lower()}")
    else:
        await message.reply("Please provide a message to whisper.")

# Команда /scream
@router.message(F.text.startswith("/scream"))
async def scream(message: Message):
    args = message.text[len("/scream "):].strip()
    if args:
        await message.reply(f"(SCREAMING): {args.upper()}!!!")
    else:
        await message.reply("Please provide a message to scream.")

# Реєстрація команд
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/menu", description="Show this menu"),
        BotCommand(command="/whisper", description="Send a quiet message"),
        BotCommand(command="/scream", description="Send a loud message")
    ]
    await bot.set_my_commands(commands)

# Запуск бота
async def main():
    dp.include_router(router)
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
