import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token = os.getenv('TOKEN'))

dp = Dispatcher()

def get_url_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


def get_text_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Купить подписку")
        ],
        [
            KeyboardButton(text="ℹ️ О боте"),
            KeyboardButton(text="📬 Подписка")
        ],
        [
            KeyboardButton(text="✉️ Поддержка")
        ],
        [
            KeyboardButton(text="Пользовательское соглашение")
        ]
    ],
    resize_keyboard=True, input_field_placeholder="Выберите нужный вариант"
)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("<b>АНАЛИТИК</b> - уникальнейший инструмент, который проводит анализ акций и даёт вам всю нужную информацию по компании.\n\n"
                         "Технический и фундаментальный анализ в одном месте👇\n\n"
                         "Для начала работы нажмите кнопку /start", parse_mode="HTML", reply_markup=kb_start)

@dp.message(F.text == "Купить подписку")
async def buy_subscribe(message: types.Message):
    await message.answer("• ВЫБЕРИТЕ ТАРИФ ПОДПИСКИ:\n\n30 дней за 1490₽ ( стандарт )"
                         "\n90 дней за <s>4500₽</s> 2490₽ ( скидка 45% )\n365 дней за <s>4500₽</s> 5990₽ ( скидка 60% )", parse_mode="HTML",
                         reply_markup=get_url_btns(btns={
                             "30 дней за 1490Р": "https://ru.wikipedia.org/wiki/%D0%90_(%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0)",
                             "90 дней за 2490Р": "https://ru.wikipedia.org/wiki/%D0%90_(%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0)",
                             "365 дней за 5990Р": "https://ru.wikipedia.org/wiki/%D0%90_(%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0)"
                         })
                         )

@dp.message(F.text == "📬 Подписка")
async def buy_subscribe(message: types.Message):
    await message.answer("Подписки ещё пока нет")

@dp.message(F.text == "ℹ️ О боте")
async def info_about_bot(message: types.Message):
    await message.answer("Краткое описание пользования ботом - https://telegra.ph/Kak-polzovatsya-botom-Insider-Crypto-07-28",
                         reply_markup=get_text_btns(btns={
                             "Реквизиты организации": "ИП Сима"
                         }))

@dp.callback_query(F.data.startswith("ИП"))
async def info_about_IP(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ КУЗНЕЦОВ ДМИТРИЙ АНДРЕЕВИЧ\n\n"
                                  "ИНН 760313456991\n\n"
                                  "ОГРН 321762700059431")

@dp.message(F.text == "✉️ Поддержка")
async def info_about_bot(message: types.Message):
    await message.answer("<b>Если у вас возникли вопросы, то пишите сюда - @insiderpomosh</b>", parse_mode="HTML")

@dp.message(F.text == "Пользовательское соглашение")
async def info_about_bot(message: types.Message):
    await message.answer("Пользовательское соглашение - https://telegra.ph/test-09-09-289")

async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.run(main())