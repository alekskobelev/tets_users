import json
import unittest
from types import SimpleNamespace

from bot import register_handlers


class FakeBot:
    def __init__(self):
        self.handlers = []
        self.documents = []
        self.messages = []

    def message_handler(self, **_filters):
        def register(handler):
            self.handlers.append(handler)
            return handler

        return register

    def send_document(self, **kwargs):
        self.documents.append(kwargs)

    def send_message(self, **kwargs):
        self.messages.append(kwargs)


class BotHandlerTests(unittest.TestCase):
    def setUp(self):
        self.bot = FakeBot()
        register_handlers(self.bot)

    def test_sends_generated_users_as_json_document(self):
        message = SimpleNamespace(chat=SimpleNamespace(id=42), text="2️⃣")

        self.bot.handlers[2](message)

        document = self.bot.documents[0]
        self.assertEqual(document["chat_id"], 42)
        self.assertEqual(document["visible_file_name"], "test_users_2.json")
        self.assertEqual(len(json.loads(document["document"].getvalue())), 2)
        self.assertEqual(len(self.bot.messages), 1)

    def test_reprompts_on_unrecognized_message(self):
        message = SimpleNamespace(chat=SimpleNamespace(id=42), text=None)

        self.bot.handlers[2](message)

        self.assertEqual(self.bot.documents, [])
        self.assertEqual(len(self.bot.messages), 1)
        self.assertIn("Не понимаю", self.bot.messages[0]["text"])

    def test_help_shows_commands_and_generation_options(self):
        message = SimpleNamespace(chat=SimpleNamespace(id=42), text="/help")

        self.bot.handlers[1](message)

        self.assertIn("/start", self.bot.messages[0]["text"])
        self.assertIn("/help", self.bot.messages[0]["text"])
        self.assertIn("1, 2, 5 или 10", self.bot.messages[0]["text"])


if __name__ == "__main__":
    unittest.main()
