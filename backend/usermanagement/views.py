from rest_framework.views import APIView
from django.shortcuts import redirect
import requests
from random import SystemRandom
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse_lazy
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from rest_framework import serializers, status
from rest_framework.response import Response
from attrs import define
import jwt
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import google_auth_oauthlib.flow
from typing import Dict, Any
from usermanagement.models import *
from django.contrib.auth import login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

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