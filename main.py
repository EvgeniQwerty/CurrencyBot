import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
import json
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = '7924767319:AAHvlHY2dydtacKZezM0ismhSl-ahTe3DCU'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: Message):
    # Создаём клавиатуру с кнопкой для перехода в мини-приложение
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Перейти в мини-приложение", web_app=types.WebAppInfo(url="https://evgeniqwerty.github.io/CurrencyBot/index.html"))]
        ],
        resize_keyboard=True
    )
    
    await message.reply(
        "Добро пожаловать в MIKKIEX Exchange! Нажмите кнопку ниже, чтобы перейти в мини-приложение для обмена валют.", 
        reply_markup=markup
    )

# Обработчик данных, отправленных из мини-приложения
@dp.message()
async def handle_all_messages(message: Message):
    logger.debug(f"Received message: {message.json()}")

    if message.web_app_data:  # Проверяем наличие данных из WebApp
        logger.info(f"Received web_app_data: {message.web_app_data.data}")
        try:
            data = json.loads(message.web_app_data.data)  # Парсим JSON данные
            logger.info(f"Parsed data: {data}")
            
            from_amount = data["from"]["amount"]
            from_currency = data["from"]["currency"]
            to_amount = data["to"]["amount"]
            to_currency = data["to"]["currency"]
            exchange_rate = data["rate"]
            
            response = (
                f"Что отдаете: {from_amount} {from_currency}\n"
                f"Что получаете: {to_amount} {to_currency}\n"
                f"Курс обмена: 1 {from_currency} = {exchange_rate} {to_currency}\n"
            )
            
            # Ответное сообщение с опцией связаться с оператором
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Связаться с оператором", url="https://t.me/evgeniqwerty")]
            ])
            
            await message.answer(response, reply_markup=markup)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            await message.reply("Произошла ошибка при обработке данных. Пожалуйста, попробуйте снова.")
        except KeyError as e:
            logger.error(f"KeyError: {e}")
            await message.reply("Произошла ошибка при обработке данных. Пожалуйста, попробуйте снова.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await message.reply("Произошла неожиданная ошибка. Пожалуйста, попробуйте снова позже.")
    else:
        logger.info(f"Received message: {message.text}")
        await message.answer("Бот работает, получил ваше сообщение!")

async def main():
    logger.info("Starting bot")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        if not loop.is_running():
            loop.run_forever()
