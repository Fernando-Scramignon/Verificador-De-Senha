from rest_framework.views import APIView
from rest_framework.response import Response
from utils.classes.password_verifier import PasswordVerifier


class VerifierViews(APIView):
    def post(self, request):
        passwordVerifier = PasswordVerifier(request.data)

        return Response(passwordVerifier.verification_info, status=200)
