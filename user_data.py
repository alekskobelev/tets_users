import json
import re
from secrets import token_urlsafe
from typing import Any

from faker import Faker

SUPPORTED_COUNTS = (1, 2, 5, 10)
PHONE_DIGITS = 10


def generate_users(count: int) -> list[dict[str, Any]]:
    if isinstance(count, bool) or count not in SUPPORTED_COUNTS:
        raise ValueError(f"count must be one of {SUPPORTED_COUNTS}")

    faker = Faker("ru_RU")
    users = []
    for _ in range(count):
        user = faker.simple_profile()
        phone_digits = re.sub(r"\D", "", faker.msisdn())
        if len(phone_digits) < PHONE_DIGITS:
            raise ValueError("Faker generated a phone number with fewer than 10 digits")

        user["phone"] = f"+7{phone_digits[-PHONE_DIGITS:]}"
        user["password"] = token_urlsafe(10)
        users.append(user)
    return users


def serialize_users(users: list[dict[str, Any]]) -> str:
    return json.dumps(
        users,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )
