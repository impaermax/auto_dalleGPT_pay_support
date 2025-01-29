from telebot import types

class PaymentModule:
    def __init__(self, bot, db, keyboards):
        self.bot = bot
        self.db = db
        self.keyboards = keyboards

    def register_handlers(self):
        @self.bot.message_handler(func=lambda msg: msg.text == '🛍 Купить генерации')
        def handle_buy_generations(message):
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton("5 генераций - 100₽", callback_data='buy_5'),
                types.InlineKeyboardButton("10 генераций - 180₽", callback_data='buy_10')
            )
            self.bot.send_message(message.chat.id, "Выберите пакет:", reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
        def process_payment(call):
            user_id = call.from_user.id
            amount = int(call.data.split('_')[1])
            self.db.cursor.execute('INSERT INTO transactions (user_id, amount) VALUES (?, ?)', (user_id, amount))
            self.db.conn.commit()
            self.bot.send_message(
                call.message.chat.id,
                f"Оплатите {amount * 20}₽ на карту 22330 33337 01332 34463",
                reply_markup=self.keyboards.payment_confirmation_keyboard()
            )
