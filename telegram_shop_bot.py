import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# ضع التوكن الخاص بك هنا
TOKEN = 8058710486:AAGVFuguZe5n_GUkY7ul_D1H
# تفعيل نظام التسجيل لمراقبة الأخطاء
logging.basicConfig(level=logging.INFO)

# إنشاء كائنات البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def start_handler(message: Message):
    if message.text == "/start":
        await message.answer("مرحبًا بك في بوت المتجر! 🛍️\nاستخدم الأوامر للبدء.")

# تشغيل البوت
async def main():
    try:
        print("✅ البوت يعمل الآن...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
