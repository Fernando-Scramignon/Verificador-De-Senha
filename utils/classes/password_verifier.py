from rest_framework.exceptions import ValidationError
import ipdb


class PasswordVerifier:

    """
    Essas são as constantes de configuração. Elas permitem facilmente escalar a aplicação,
    extendendo uma outra classe dessa e adicionando mais regras e validadores
    """

    # Os campos necessários para a requisição
    REQUIRED_FIELDS = ["password", "rules"]

    # As regras permitidas
    ALLOWED_RULES = [
        "minSize",
        "minUpperCase",
        "minLowerCase",
        "minDigit",
        "minSpecialChars",
        # tem dois aqui por causa de um erro de escrita no enunciado do desafio
        "noRepeted",
        "noRepeated",
    ]

    """
    Esse próximo setor são os validadores individuais. Cada um tem a sua lógica.
    Porém todos terminam mais ou menos do mesmo jeito. Se falhar, transformar
    a propriedade verify (propriedade de instância) para false e adiciona o nome do erro
    para no_match_list(proriedade de instância).
    """

    def validate_no_repeated(self, password: str, value: int) -> None:
        """
        Esse aqui itera sobre todos os caracteres menos o último e verifica se
        o atual é igual ao sucessor, se for adiciona 1 à variável repeated_count.
        Caso repeated_count seja maior que 1, quer dizer que essa vericação reprovou a senha
        """

        repeated_count = 0

        for index in range(len(password) - 1):
            current_char = password[index]
            next_char = password[index + 1]

            if current_char == next_char:
                repeated_count += 1

        if repeated_count:
            self.verify = False
            self.no_match_list.append("noRepeated")

    def validate_min_special_chars(self, password: str, value: int) -> None:
        """
        Itera sobre todos os caracteres e vê se ele está em special_chars_list (variável)
        Se estiver, adiciona 1 para special_chars_count (variável) e ela for menor que o
        argumento value, a senha é reprovada.
        """

        special_chars_list = "!@#$%^&*()-+\/{}[]"
        special_chars_count = 0

        for char in password:
            if char in special_chars_list:
                special_chars_count += 1

        if special_chars_count < value:
            self.verify = False
            self.no_match_list.append("minSpecialChars")

    def validate_min_digit(self, password: str, value: int) -> None:
        """
        Se algum caractere da senha estiver contido na lista de digitos, o valor um é adicionado
        para a contagem de digitos. Se a contagem de digitos for menor que o argumento value, a
        senha é reprovada.
        """

        digits_list = [str(n) for n in range(10)]
        digits_count = 0

        for char in password:
            if char in digits_list:
                digits_count += 1

        if digits_count < value:
            self.verify = False
            self.no_match_list.append("minDigit")

    def validate_min_size(self, password: str, value: int) -> None:
        """
        Verifica se o tamanho da senha é menor que o argumento value. Se for, a senha é reprovada.
        """

        if len(password) < value:
            self.verify = False
            self.no_match_list.append("minSize")

    def validate_min_upper_case(self, password: str, value: int) -> None:
        """
        Itera sobre os caracteres da senha e se o caracter estiver em uppercase,
        adiciona um para o contador. Se o contador for menor que value, a senha é reprovada
        """
        upper_case_chars_count = 0

        for char in password:
            if char.isupper():
                upper_case_chars_count += 1

        if upper_case_chars_count < value:
            self.verify = False
            self.no_match_list.append("minUpperCase")

    def validate_min_lower_case(self, password: str, value: int) -> None:
        """
        Itera sobre os caracteres da senha e se ele estiver em lowercase,
        adiciona 1 ao contador. Se o contador for menor que value, a senha é reprovada
        """

        lower_case_chars_count = 0

        for char in password:
            if char.islower():
                lower_case_chars_count += 1

        if lower_case_chars_count < value:
            self.verify = False
            self.no_match_list.append("minLowerCase")

    def verify_request(self, data: dict) -> None:
        """
        Verifica se têm alguma chave faltando na requisição, se sim, levanta um erro
        que é automaticamente captado pelo django.
        """

        for field in self.REQUIRED_FIELDS:
            if not data.get(field):
                raise ValidationError({"message": "Missing key: " + field})

    def validate_data(self, data: dict):
        """
        Esse aqui vê se as regras estão em formato certo. Depois vê se as regras passados
        são permitidas pelo ALLOWED_RULES, se sim ele chama a função de validação certa
        utilizando o RULES_MAP (dicionário onde as regras são as chaves e os valores são as funções de validação)
        """

        rules = data["rules"]
        password = data["password"]

        for rule_dict in rules:
            if not isinstance(rule_dict, dict):
                raise ValidationError({"message": f"{rule_dict} is not a dictionary"})

            if not rule_dict.get("rule"):
                raise ValidationError(
                    {"message": "Rule in wrong format. Missing 'rule' key"}
                )

            if not rule_dict.get("value") and rule_dict.get("value") != 0:
                raise ValidationError(
                    {"message": "Rule in wrong format. Missing 'value' key"}
                )

            if not isinstance(rule_dict["value"], int):
                raise ValidationError({"message": "Value must be an integer"})

            rule = rule_dict["rule"]
            value = rule_dict["value"]

            if rule not in self.ALLOWED_RULES:
                raise ValidationError(
                    {"message": f"rule: {rule} is not an allowed rule"}
                )

            # Usa o nome da regra e um dicinário que liga cada regra à sua função validadora
            # Isso foi feito para diminuir o número de ifs e fazer o código ficar mais fácil de modificar
            self.RULES_MAP[rule](self, password, value)

    RULES_MAP = {
        "minSize": validate_min_size,
        "minUpperCase": validate_min_upper_case,
        "minLowerCase": validate_min_lower_case,
        "minDigit": validate_min_digit,
        "minSpecialChars": validate_min_special_chars,
        # Aqui tem dois no repeated, pois tem um erro de escrita no enunciado da prova
        # Pra não ter problema eu coloquei os dois
        "noRepeted": validate_no_repeated,
        "noRepeated": validate_no_repeated,
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
