import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Text

# ضع التوكن الخاص بك هنا
TOKEN = "8058710486:AAGVFuguZe5n_GUkY7ul_D1HXpk8QX6ST-U"

# تفعيل نظام التسجيل لمراقبة الأخطاء
logging.basicConfig(level=logging.INFO)

# إنشاء كائنات البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

# إنشاء كيبورد يحتوي على زر "📞 اتصل بنا"
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 اتصل بنا")],
    ],
    resize_keyboard=True
)

# معلومات الاتصال
CONTACT_INFO = """
📞 **معلومات الاتصال:**
📌 هاتف المبيعات: 07705999075 - 07834083540
🌐 للتسوق عبر التطبيق: [اضغط هنا](https://www.telosshop.com)
🔵 زيارة صفحتنا على الفيس بوك: [اضغط هنا](https://www.facebook.com/share/1RfvHRMBNr/?mibextid=wwXIfr)
🛠 **الدعم التقني:** 07831922418
🕔 **أوقات الدوام:** من الساعة 9 صباحًا لغاية 4 مساءً
"""

# أمر /start للترحيب بالمستخدم
@dp.message_handler(commands=["start"])
async def start_handler(message: Message):
    await message.answer(
        "مرحبًا بك في بوت المتجر! 🛍️\nاستخدم الأوامر أو الزر أدناه للبدء.", 
        reply_markup=contact_keyboard
    )

# أمر /contact لعرض معلومات الاتصال
@dp.message_handler(commands=["contact"])
async def contact_command_handler(message: Message):
    await message.answer(CONTACT_INFO, parse_mode="Markdown")

# التعامل مع زر "📞 اتصل بنا"
@dp.message_handler(Text(equals="📞 اتصل بنا"))
async def contact_button_handler(message: Message):
    await message.answer(CONTACT_INFO, parse_mode="Markdown")

# تشغيل البوت
async def main():
    print("✅ البوت يعمل الآن...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
