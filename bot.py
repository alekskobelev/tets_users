from io import BytesIO

from telebot import TeleBot, types

from user_data import generate_users, serialize_users

BUTTON_COUNTS = {
    "1️⃣": 1,
    "2️⃣": 2,
    "5️⃣": 5,
    "🔟": 10,
}
HELP_TEXT = (
    "Я создаю синтетические данные пользователей и отправляю их JSON-файлом.\n"
    "Доступно 1, 2, 5 или 10 пользователей.\n\n"
    "Команды:\n"
    "/start — открыть меню\n"
    "/help — показать эту справку"
)


def create_menu() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton(text="1️⃣"),
        types.KeyboardButton(text="2️⃣"),
    )
    markup.row(
        types.KeyboardButton(text="5️⃣"),
        types.KeyboardButton(text="🔟"),
    )
    return markup


def register_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["start"])
    def handle_start(message: types.Message) -> None:
        bot.send_message(
            chat_id=message.chat.id,
            text=(
                "Привет! Это бот для генерации тестовых пользователей. "
                "Выбери нужное количество 👇"
            ),
            reply_markup=create_menu(),
        )

    @bot.message_handler(commands=["help"])
    def handle_help(message: types.Message) -> None:
        bot.send_message(
            chat_id=message.chat.id,
            text=HELP_TEXT,
            reply_markup=create_menu(),
        )

    @bot.message_handler(func=lambda _message: True)
    def handle_message(message: types.Message) -> None:
        count = BUTTON_COUNTS.get(message.text or "")
        if count is None:
            bot.send_message(
                chat_id=message.chat.id,
                text="Не понимаю тебя. Выбери количество пользователей на клавиатуре.",
                reply_markup=create_menu(),
            )
            return

        payload = serialize_users(generate_users(count))
        document = BytesIO(payload.encode("utf-8"))
        bot.send_document(
            chat_id=message.chat.id,
            document=document,
            visible_file_name=f"test_users_{count}.json",
            caption=f"Данные {count} тестовых пользователей.",
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Если нужны еще данные, выбери количество 👇",
            reply_markup=create_menu(),
        )


def create_bot(token: str) -> TeleBot:
    bot = TeleBot(token)
    register_handlers(bot)
    return bot
