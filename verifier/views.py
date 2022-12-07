from rest_framework.views import APIView
from rest_framework.response import Response

# A lógica da applicação está aqui
from utils.classes.password_verifier import PasswordVerifier


"""
Os comentários em português são para documentar a lógica de implementação
como foi pedido no enunciado do desafio técnico.
Normalmente eu não comento tanto assim :)
No README tem as informações para o código ser rodade e como funciona.
Caso não tenha um leitor de markdown. Esse é o repositório do projeto:
https://github.com/Fernando-Scramignon/verificador_de_senha
"""


class VerifierViews(APIView):
    def post(self, request):
        """
        Cria uma instância do validador de senhas se a requisição conter informações erradas
        ele levanta um validationError que é capturado automaticamente pelo django e retorna uma
        resposta 400 BAD REQUEST. Caso tudo esteja certo,  o resultado da verificação fica na propriedade
        verification_info (mesmo se alguma validação falhou).
        """
        passwordVerifier = PasswordVerifier(request.data)
        return Response(passwordVerifier.verification_info, status=200)
