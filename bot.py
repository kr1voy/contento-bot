import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "СКРЫТО"

bot = Bot(token=TOKEN)
dp = Dispatcher()

platforms = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Instagram"), KeyboardButton(text="TikTok")],
        [KeyboardButton(text="Telegram"), KeyboardButton(text="YouTube")],
        [KeyboardButton(text="Другое")]
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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())