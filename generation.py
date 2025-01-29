class GenerationModule:
    def __init__(self, bot, db, keyboards, image_generator):
        self.bot = bot
        self.db = db
        self.keyboards = keyboards
        self.image_generator = image_generator

    def register_handlers(self):
        @self.bot.message_handler(func=lambda msg: msg.text == '🎨 Сгенерировать изображение')
        def handle_generate_image(message):
            user_id = message.from_user.id
            user = self.db.get_user(user_id)
            if user and user[3]:  # Проверка is_approved
                msg = self.bot.send_message(message.chat.id, "Введите описание изображения:")
                self.bot.register_next_step_handler(msg, self.process_image_generation)
            else:
                self.bot.send_message(message.chat.id, "❌ Ваш аккаунт не подтвержден!")

    def process_image_generation(self, message):
        user_id = message.from_user.id
        user = self.db.get_user(user_id)
        if user and user[2] > 0:  # Проверка баланса
            result = self.image_generator.generate_image(message.text)
            if "error" not in result:
                self.bot.send_photo(message.chat.id, photo=result[0])
                self.db.update_balance(user_id, -1)
            else:
                self.bot.send_message(message.chat.id, f"⚠️ Ошибка: {result['error']}")
        else:
            self.bot.send_message(message.chat.id, "❌ Недостаточно генераций!")
