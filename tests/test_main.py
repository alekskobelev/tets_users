import os
import unittest
from unittest.mock import Mock, patch

from main import main


class MainTests(unittest.TestCase):
    def test_requires_bot_token(self):
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": ""}):
            with self.assertRaisesRegex(RuntimeError, "TELEGRAM_BOT_TOKEN"):
                main()

    def test_creates_bot_and_starts_polling(self):
        bot = Mock()
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test-token"}):
            with patch("main.create_bot", return_value=bot) as create_bot:
                main()

        create_bot.assert_called_once_with("test-token")
        bot.infinity_polling.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
