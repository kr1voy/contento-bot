import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = "/webhook"

if not TOKEN:
    raise ValueError("Не задан BOT_TOKEN")

if not WEBHOOK_URL:
    raise ValueError("Не задан RENDER_EXTERNAL_URL")

bot = Bot(token=TOKEN)
dp = Dispatcher()

platforms = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Instagram"),
            KeyboardButton(text="TikTok")
        ],
        [
            KeyboardButton(text="Telegram"),
            KeyboardButton(text="YouTube")
        ],
        [
            KeyboardButton(text="Другое")
        ]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я CONTENTO 👋\n"
        "Помогу придумать идеи для твоего контента.\n"
        "Выбери площадку:",
        reply_markup=platforms
    )

@dp.message()
async def choose_platform(message: Message):
    await message.answer(
        f"Отлично! Ты выбрал: {message.text}\n"
        "Теперь напиши, о чём твой блог."
    )

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")

async def main():
    dp.startup.register(on_startup)

    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000"))
    )

if __name__ == "__main__":
    asyncio.run(main())
