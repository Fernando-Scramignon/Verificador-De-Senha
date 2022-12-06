import ipdb
from rest_framework.exceptions import ValidationError


class PasswordVerifier:
    REQUIRED_FIELDS = ["password", "rules"]

    ALLOWED_RULES = [
        "minSize",
        "minUpperCase",
        "minLowerCase",
        "minDigit",
        "minSpecialChars",
        "noRepeted",
    ]

    def validate_no_repeted(self, password: str, value: int) -> None:
        repeated_count = 0

        for index in range(len(password) - 1):
            current_char = password[index]
            next_char = password[index + 1]

            if current_char == next_char:
                repeated_count += 1

        if repeated_count:
            self.verify = False
            self.no_match_list.append("noRepeted")

    def validate_min_special_chars(self, password: str, value: int) -> None:
        special_chars_list = "!@#$%^&*()-+\/{}[]"
        special_chars_count = 0

        for char in password:
            if char in special_chars_list:
                special_chars_count += 1

        if special_chars_count < value:
            self.verify = False
            self.no_match_list.append("minSpecialChars")

    def validate_min_digit(self, password: str, value: int) -> None:
        digits_list = [str(n) for n in range(10)]
        digits_count = 0

        for char in password:
            if char in digits_list:
                digits_count += 1

        if digits_count < value:
            self.verify = False
            self.no_match_list.append("minDigit")

    def validate_min_size(self, password: str, value: int) -> None:
        if len(password) < value:
            self.verify = False
            self.no_match_list.append("minSize")

    def validate_min_upper_case(self, password: str, value: int) -> None:
        upper_case_chars_count = 0

        for char in password:
            if char.isupper():
                upper_case_chars_count += 1

        if upper_case_chars_count < value:
            self.verify = False
            self.no_match_list.append("minUpperCase")

    def validate_min_lower_case(self, password: str, value: int) -> None:
        lower_case_chars_count = 0

        for char in password:
            if char.islower():
                lower_case_chars_count += 1

        if lower_case_chars_count < value:
            self.verify = False
            self.no_match_list.append("minLowerCase")

    def verify_request(self, data: dict) -> None:
        for field in self.REQUIRED_FIELDS:
            if not data.get(field):
                raise ValidationError({"message": "Missing key: " + field})

    def validate_data(self, data: dict):
        rules = data["rules"]
        password = data["password"]

        for rule_dict in rules:
            if not (type(rule_dict) is dict):
                raise ValidationError({"message": f"{rule_dict} is not a dictionary"})

            rule = rule_dict["rule"]
            value = rule_dict["value"]

            if rule not in self.ALLOWED_RULES:
                raise ValidationError(
                    {"message": f"rule: {rule} is not an allowed rule"}
                )

            self.RULES_MAP[rule](self, password, value)

    RULES_MAP = {
        "minSize": validate_min_size,
        "minUpperCase": validate_min_upper_case,
        "minLowerCase": validate_min_lower_case,
        "minDigit": validate_min_digit,
        "minSpecialChars": validate_min_special_chars,
        "noRepeted": validate_no_repeted,
    }

    def __init__(self, data):
        self.no_match_list = []

        self.verify = True

        # checks if needed keys are present
        self.verify_request(data)

        # validates password
        self.validate_data(data)

        # result
        self.verification_info = {"verify": self.verify, "noMatch": self.no_match_list}
