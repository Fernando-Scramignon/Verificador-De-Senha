from django.test import TestCase
from utils.classes.password_verifier import PasswordVerifier

"""
To run tests type in the terminal: python manage.py test
"""


class PasswordVerifierTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.fail_min_size_rule_data = {
            "input": {"password": "12345", "rules": [{"rule": "minSize", "value": 7}]},
            "expected_output": {"verify": False, "noMatch": ["minSize"]},
        }

        cls.success_min_size_rule_data = {
            "input": {
                "password": "1234567",
                "rules": [{"rule": "minSize", "value": 7}],
            },
            "expected_output": {"verify": True, "noMatch": []},
        }

        cls.fail_min_upper_case_rule_data = {
            "input": {
                "password": "CoolPassword",
                "rules": [{"rule": "minUpperCase", "value": 3}],
            },
            "expected_output": {"verify": False, "noMatch": ["minUpperCase"]},
        }

        cls.success_min_upper_case_rule_data = {
            "input": {
                "password": "CoolPassword",
                "rules": [{"rule": "minUpperCase", "value": 2}],
            },
            "expected_output": {"verify": True, "noMatch": []},
        }
        cls.fail_min_lower_case_rule_data = {
            "input": {
                "password": "cOOLpASSWORD",
                "rules": [{"rule": "minLowerCase", "value": 3}],
            },
            "expected_output": {"verify": False, "noMatch": ["minLowerCase"]},
        }

        cls.success_min_lower_case_rule_data = {
            "input": {
                "password": "cOOLpASSWORD",
                "rules": [{"rule": "minLowerCase", "value": 2}],
            },
            "expected_output": {"verify": True, "noMatch": []},
        }

        cls.fail_min_digit_rule_data = {
            "input": {
                "password": "password123",
                "rules": [{"rule": "minDigit", "value": 4}],
            },
            "expected_output": {"verify": False, "noMatch": ["minDigit"]},
        }

        cls.success_min_digit_rule_data = {
            "input": {
                "password": "password123",
                "rules": [{"rule": "minDigit", "value": 3}],
            },
            "expected_output": {"verify": True, "noMatch": []},
        }

        cls.fail_min_special_chars_rule_data = {
            "input": {
                "password": "password!@#",
                "rules": [{"rule": "minSpecialChars", "value": 4}],
            },
            "expected_output": {"verify": False, "noMatch": ["minSpecialChars"]},
        }

        cls.success_min_special_chars_rule_data = {
            "input": {
                "password": "password!@#",
                "rules": [{"rule": "minSpecialChars", "value": 3}],
            },
            "expected_output": {"verify": True, "noMatch": []},
        }

        cls.fail_no_repeated_rule_data = {
            "input": {
                "password": "coolPassword",
                "rules": [{"rule": "noRepeated", "value": 0}],
            },
            "expected_output": {"verify": False, "noMatch": ["noRepeated"]},
        }

        cls.success_no_repeated_rule_data = {
            "input": {
                "password": "qwerty",
                "rules": [{"rule": "noRepeated", "value": 0}],
            },
            "expected_output": {"verify": True, "noMatch": []},
        }

        cls.fail_all_rules_data = {
            "input": {
                "password": "StrongPassword@!#123",
                "rules": [
                    {"rule": "minUpperCase", "value": 3},
                    {"rule": "minLowerCase", "value": 14},
                    {"rule": "minDigit", "value": 4},
                    {"rule": "minSpecialChars", "value": 4},
                    {"rule": "noRepeated", "value": 0},
                    {"rule": "minSize", "value": 22},
                ],
            },
            "expected_output": {
                "verify": False,
                "noMatch": [
                    "minUpperCase",
                    "minLowerCase",
                    "minDigit",
                    "minSpecialChars",
                    "noRepeated",
                    "minSize",
                ],
            },
        }

        cls.success_all_rules_data = {
            "input": {
                "password": "Portal 2!",
                "rules": [
                    {"rule": "minUpperCase", "value": 1},
                    {"rule": "minLowerCase", "value": 5},
                    {"rule": "minDigit", "value": 1},
                    {"rule": "minSpecialChars", "value": 1},
                    {"rule": "noRepeated", "value": 0},
                    {"rule": "minSize", "value": 9},
                ],
            },
            "expected_output": {"verify": True, "noMatch": []},
        }

        cls.mixed_outcome_data = {
            "input": {
                "password": "persona 5",
                "rules": [
                    {"rule": "minUpperCase", "value": 1},
                    {"rule": "minDigit", "value": 1},
                    {"rule": "minSpecialChars", "value": 1},
                    {"rule": "noRepeated", "value": 0},
                ],
            },
            "expected_output": {
                "verify": False,
                "noMatch": ["minUpperCase", "minSpecialChars"],
            },
        }

    def test_min_size_rule(self):
        # failure
        input = self.fail_min_size_rule_data["input"]
        expected_output = self.fail_min_size_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

        # success
        input = self.success_min_size_rule_data["input"]
        expected_output = self.success_min_size_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

    def test_min_upper_case_rule(self):
        # failure
        input = self.fail_min_upper_case_rule_data["input"]
        expected_output = self.fail_min_upper_case_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

        # success
        input = self.success_min_upper_case_rule_data["input"]
        expected_output = self.success_min_upper_case_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

    def test_min_lower_case_rule(self):
        # failure
        input = self.fail_min_lower_case_rule_data["input"]
        expected_output = self.fail_min_lower_case_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

        # success
        input = self.success_min_lower_case_rule_data["input"]
        expected_output = self.success_min_lower_case_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

    def test_min_digit_rule(self):
        # failure
        input = self.fail_min_digit_rule_data["input"]
        expected_output = self.fail_min_digit_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

        # success
        input = self.success_min_digit_rule_data["input"]
        expected_output = self.success_min_digit_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

    def test_min_special_chars_rule(self):
        # failure
        input = self.fail_min_special_chars_rule_data["input"]
        expected_output = self.fail_min_special_chars_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

        # success
        input = self.success_min_special_chars_rule_data["input"]
        expected_output = self.success_min_special_chars_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

    def test_no_repeated_rule(self):
        # failure
        input = self.fail_no_repeated_rule_data["input"]
        expected_output = self.fail_no_repeated_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

        # success
        input = self.success_no_repeated_rule_data["input"]
        expected_output = self.success_no_repeated_rule_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

    def test_all_rules(self):

        # failure
        input = self.fail_all_rules_data["input"]
        expected_output = self.fail_all_rules_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

        # success
        input = self.success_all_rules_data["input"]
        expected_output = self.success_all_rules_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)

    def test_mixed_output(self):
        input = self.mixed_outcome_data["input"]
        expected_output = self.mixed_outcome_data["expected_output"]

        passwordVerifier = PasswordVerifier(input)
        self.assertEqual(passwordVerifier.verification_info, expected_output)
