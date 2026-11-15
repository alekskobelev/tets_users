import logging
import os

from bot import create_bot


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Set the TELEGRAM_BOT_TOKEN environment variable before starting the bot."
        )

    bot = create_bot(token)
    bot.infinity_polling()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    main()
