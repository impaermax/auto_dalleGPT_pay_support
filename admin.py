class AdminModule:
    def __init__(self, bot, db, keyboards, admin_id):
        self.bot = bot
        self.db = db
        self.keyboards = keyboards
        self.admin_id = admin_id

    def register_handlers(self):
        @self.bot.message_handler(commands=['admin'])
        def handle_admin(message):
            if message.from_user.id == self.admin_id:
                self.bot.send_message(message.chat.id, "Админ-панель:", reply_markup=self.keyboards.admin_keyboard())

        @self.bot.message_handler(func=lambda msg: msg.text == '👥 Пользователи')
        def handle_users_list(message):
            if message.from_user.id == self.admin_id:
                users = self.db.cursor.execute('SELECT user_id, username, is_approved FROM users').fetchall()
                response = "Список пользователей:\n"
                for user in users:
                    response += f"@{user[1]} - {'Активен' if user[2] else 'Не активен'}\n"
                self.bot.send_message(message.chat.id, response)
