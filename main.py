import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton ,InlineKeyboardMarkup

from config import Bot_token

user_carts = {}

user_main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="🍴 Menyu")
    ]
    ,
    [
        KeyboardButton(text="📋 Mening buyurtmalarim")
    ],
    [
        KeyboardButton(text="📥 Savat"),
        KeyboardButton(text="for 📞 Aloqa")
    ],
    [
        KeyboardButton(text="📨 Xabar yuborish"),
        KeyboardButton(text="⚙️ Sozlamalar")
    ]

],
resize_keyboard=True,
is_persistent=True
)

user_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Setlar")
    ],
    [
        KeyboardButton(text="Lavash"),
        KeyboardButton(text="burger")
    ],
    [
        KeyboardButton(text="🔙 Orqaga qaytish")
    ]
],
    resize_keyboard=True,
    is_persistent=True)



lavash_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Mini 22 000 so'm ", callback_data="lavash mini"),
        InlineKeyboardButton(text="Original 26 000 so'm ", callback_data="lavash original")
    ]
])


async def start_handler(message: types.Message, bot: Bot):
    text = f"EVOS | Доставка botiga xush kelibsiz! {message.from_user.mention_html(f'{message.from_user.full_name}')}"
    await message.answer(text=text, parse_mode="HTML", reply_markup=user_main_keyboard)
    await message.answer(text="🛒 Asosiy Menyu")
    await message.answer(text="Marhamat buyurtma berishingiz mumkin!")


async def menu_handler(message: types.Message):
    text = "Menu bosildi, tanlang :"
    await message.answer(text=text, reply_markup=user_menu_keyboard)


async def back_handler(message: types.Message):
    text = "🛒 Asosiy Menyu"
    await message.answer(text=text, reply_markup=user_main_keyboard)


async def handler_lavash(message: types.Message):
    await message.answer("Tanlang :", reply_markup=lavash_inline_keyboard)

async def mini_lavash_callback(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    product = "Mini lavash - 22 000 so'm "

    user_carts.setdefault(user_id, []).append(product)

    await callback.answer("✅ Mini Lavash savatga qo‘shildi.")
    await callback.message.answer("Mini lavash savatga qo'shildi.")

async def lavash_big_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    product = "Lavash - 26 000 so'm "

    user_carts.setdefault(user_id, []).append(product)

    await callback.answer("✅ Big Lavash savatga qo‘shildi.")
    await callback.message.answer("Big Lavash savatga qo‘shildi.")

async def savat_handler(message: types.Message):
    await message.answer("Siz savat tugmasini bosdingiz", reply_markup=user_main_keyboard)


async def main():
    bot = Bot(token=Bot_token)
    dp = Dispatcher()
    dp.message.register(start_handler, Command('start'))
    dp.message.register(menu_handler, F.text == "🍴 Menyu")
    dp.message.register(back_handler, F.text == "🔙 Orqaga qaytish")
    dp.message.register(handler_lavash, F.text == "Lavash")
    dp.message.register(savat_handler, F.text == "📥 Savat")


    dp.callback_query.register(mini_lavash_callback, F.text == "lavash mini")
    dp.callback_query.register(lavash_big_callback, F.text == "lavash original")

    await dp.start_polling(bot, polling_timeout=0)


if __name__ == '__main__':
    asyncio.run(main())