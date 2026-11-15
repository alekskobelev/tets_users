from datetime import date
import json
import re
import unittest

from user_data import SUPPORTED_COUNTS, generate_users, serialize_users


class GenerateUsersTests(unittest.TestCase):
    def test_generates_requested_number_of_users_with_valid_phone_and_password(self):
        for count in SUPPORTED_COUNTS:
            with self.subTest(count=count):
                users = generate_users(count)

                self.assertEqual(len(users), count)
                for user in users:
                    self.assertRegex(user["phone"], re.compile(r"\+7\d{10}"))
                    self.assertTrue(user["password"])
                    self.assertIn("name", user)
                    self.assertIn("mail", user)
                    self.assertIn("address", user)

    def test_rejects_unsupported_counts(self):
        for count in (0, 3, 11, True):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    generate_users(count)

    def test_serializes_unicode_and_non_json_values(self):
        payload = serialize_users([{"name": "Иван", "birthdate": date(2000, 1, 2)}])

        self.assertIn("Иван", payload)
        self.assertNotIn("\\u", payload)
        self.assertEqual(json.loads(payload)[0]["birthdate"], "2000-01-02")


if __name__ == "__main__":
    unittest.main()
