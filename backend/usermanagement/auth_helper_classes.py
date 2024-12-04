from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from attrs import define
import jwt
from typing import Dict, Any

class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()

@define
class GoogleAccessTokens:
    id_token: str
    access_token: str
    def decode_id_token(self) -> Dict[str, Any]:
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
        return decoded_token

class CustomAuthToken(ObtainAuthToken):
    """
    Generates or retrieves an authentication token for a user.

    This function validates the user's credentials, creates a token if it 
    doesn't exist, and returns the token along with the user ID and email.

    Parameters:
        request (Request): The HTTP request object containing user credentials.
        args: Positional arguments.
        kwargs: Keyword arguments.

    Returns:
        Response: A JSON response containing:
            - token (str): The authentication token.
            - user_id (int): The user's ID.
            - email (str): The user's email address.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
