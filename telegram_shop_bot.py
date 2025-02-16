import sqlite3
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram import Bot, Dispatcher

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())


# إعدادات البوت
TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        image TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        address TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# عرض المنتجات
def get_products():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

@dp.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    products = get_products()
    for product in products:
        keyboard.add(InlineKeyboardButton(f"{product[1]} - {product[2]}$", callback_data=f"product_{product[0]}"))
    bot.send_message(message.chat.id, "مرحبًا! اختر المنتج الذي تريده:", reply_markup=keyboard)

@dp.message_handler(commands=['products'])
def list_products(message: types.Message):
    products = get_products()
    if not products:
        bot.send_message(message.chat.id, "لا توجد منتجات متاحة حاليًا.")
        return
    for product in products:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("شراء الآن", callback_data=f"buy_{product[0]}"))
        bot.send_photo(message.chat.id, product[3], caption=f"{product[1]}\nالسعر: {product[2]}$", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith("buy_"))
def buy_product(call: types.CallbackQuery):
    product_id = int(call.data.split("_")[1])
    bot.send_message(call.message.chat.id, "أدخل عنوان التوصيل:")
    
    @dp.message_handler(content_types=types.ContentType.TEXT)
    def save_order(message: types.Message):
        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, product_id, quantity, address) VALUES (?, ?, ?, ?)",
                       (message.from_user.id, product_id, 1, message.text))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "تم استلام طلبك بنجاح! سيتم التواصل معك قريبًا.")

@dp.message_handler(commands=['help'])
def send_help(message: types.Message):
    bot.send_message(message.chat.id, "\nالاوامر المتاحة:\n/start - بدء البوت\n/products - عرض المنتجات\n/order - تقديم طلب\n/help - المساعدة\n/add_product - إضافة منتج جديد")

@dp.message_handler(commands=['add_product'])
def add_product(message: types.Message):
    bot.send_message(message.chat.id, "أدخل اسم المنتج:")
    
    @dp.message_handler(content_types=types.ContentType.TEXT)
    def get_product_name(msg: types.Message):
        product_name = msg.text
        bot.send_message(msg.chat.id, "أدخل سعر المنتج:")
        
        @dp.message_handler(content_types=types.ContentType.TEXT)
        def get_product_price(msg2: types.Message):
            try:
                product_price = float(msg2.text)
                bot.send_message(msg2.chat.id, "أدخل رابط صورة المنتج:")
                
                @dp.message_handler(content_types=types.ContentType.TEXT)
                def get_product_image(msg3: types.Message):
                    product_image = msg3.text
                    conn = sqlite3.connect("shop.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO products (name, price, image) VALUES (?, ?, ?)", (product_name, product_price, product_image))
                    conn.commit()
                    conn.close()
                    bot.send_message(msg3.chat.id, "✅ تم إضافة المنتج بنجاح!")
                
            except ValueError:
                bot.send_message(msg2.chat.id, "⚠️ يجب إدخال سعر صحيح بالأرقام فقط.")

# تشغيل البوت
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
   import asyncio

async def main():
    await dp.start_polling()

import asyncio

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
