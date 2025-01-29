from telebot import types

class Keyboards:
    @staticmethod
    def main_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('🎨 Сгенерировать изображение')
        keyboard.add('💰 Баланс', '🛍 Купить генерации')
        keyboard.add('🆘 Техподдержка', 'ℹ️ Помощь')
        return keyboard

    @staticmethod
    def admin_keyboard():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('👥 Пользователи', '📊 Статистика')
        keyboard.add('⏳ Заявки на регистрацию', '📨 Рассылка')
        return keyboard

    @staticmethod
    def registration_decision_keyboard(user_id):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("✅ Одобрить", callback_data=f'approve_{user_id}'),
            types.InlineKeyboardButton("❌ Отклонить", callback_data=f'reject_{user_id}')
        )
        return keyboard

    @staticmethod
    def payment_confirmation_keyboard():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("✅ Я оплатил", callback_data='check_payment')
        )
        return keyboard

    @staticmethod
    def support_response_keyboard(user_id):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("✉️ Ответить", url=f'tg://user?id={user_id}')
        )
        return keyboard
