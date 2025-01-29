import telebot
from telebot import types
import logging
from modules.database import Database
from modules.keyboards import Keyboards
from modules.recraft_image_generator import RecraftImageGenerator
from modules.admin import AdminModule
from modules.generation import GenerationModule
from modules.payment import PaymentModule

# Конфигурация
TELEGRAM_BOT_TOKEN = '7937346503:AAGj7dW3lOMbfTv4XO0W-Jr_rPDB9b8sA_A'
RECRAFT_API_KEY = 'sk-UVIYsQxzj3FqmwuSB1yrYEOlOX1tmgK023Y8Lg4SgkEb5bkgW80DWAK8vbPM'
ADMIN_ID = 1200223081

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Инициализация модулей
db = Database()
keyboards = Keyboards()
image_generator = RecraftImageGenerator(RECRAFT_API_KEY)
admin_module = AdminModule(bot, db, keyboards, ADMIN_ID)
generation_module = GenerationModule(bot, db, keyboards, image_generator)
payment_module = PaymentModule(bot, db, keyboards)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    if not db.get_user(user_id):
        db.add_user(user_id, username)
        bot.send_message(
            ADMIN_ID,
            f"Новая заявка на регистрацию!\nПользователь: @{username}",
            reply_markup=keyboards.registration_decision_keyboard(user_id)
        )
        bot.send_message(
            message.chat.id,
            "✅ Ваша заявка отправлена на модерацию. Ожидайте подтверждения!",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Главное меню:",
            reply_markup=keyboards.main_keyboard()
        )

# Обработчик техподдержки
@bot.message_handler(func=lambda msg: msg.text == '🆘 Техподдержка')
def handle_support(message):
    msg = bot.send_message(message.chat.id, "Опишите вашу проблему:")
    bot.register_next_step_handler(msg, process_support_request)

def process_support_request(message):
    user_id = message.from_user.id
    db.add_support_ticket(user_id, message.text)
    bot.send_message(
        ADMIN_ID,
        f"Новое обращение от @{message.from_user.username}:\n{message.text}",
        reply_markup=keyboards.support_response_keyboard(user_id)
    )
    bot.send_message(message.chat.id, "✅ Ваше обращение отправлено!", reply_markup=keyboards.main_keyboard())

# Подключение обработчиков из модулей
admin_module.register_handlers()
generation_module.register_handlers()
payment_module.register_handlers()

# Запуск бота
if __name__ == '__main__':
    logger.info("Бот запущен")
    bot.infinity_polling()
