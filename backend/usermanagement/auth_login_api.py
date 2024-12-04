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
from .auth_helper_classes import PublicApi, CustomAuthToken, GoogleAccessTokens

class GoogleLoginRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
        """
        Handles Google OAuth2 signup redirection.

        This function validates the user's role and associated query parameters 
        (such as school_id, year, disability, etc.), stores relevant data in the 
        session for callback processing, generates an authorization URL for Google OAuth2, 
        and redirects the user to the consent screen.

        Parameters:
            request (Request): The HTTP request object containing query parameters.
            args: Positional arguments.
            kwargs: Keyword arguments.

        Returns:
            Response: Redirects to Google's authorization URL.
            HTTP 400 Response: If required fields are missing or invalid.
        """
        role = request.GET.get("role")

        if not role:
            return Response(
                {"error": "Role is required for login."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if role not in ["student", "professor", "teacher_assistant", "sds_coordinator"]:
            return Response(
                {"error": "Invalid role provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Store role in session for later validation during callback
        request.session["form_data"] = {"role": role}

        google_login_flow = GoogleSdkLoginFlowService()
        authorization_url, state = google_login_flow.get_authorization_url()

        # Store the OAuth state in session
        request.session["google_oauth2_state"] = state

        return redirect(authorization_url)
    
class GoogleLoginApi(PublicApi):
    """Serializer For The Input --> data is validated"""
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=True)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=True)
        role = serializers.CharField(required=True)

    def get(self, request, *args, **kwargs):
        """
        Handles Google OAuth2 sign-in callback.

        This function processes the callback request from Google, validates the 
        provided tokens and state, retrieves or creates a user based on their role, 
        generates an authentication token, and redirects the user to the appropriate 
        client-side URL.

        Parameters:
            request (Request): The HTTP request object containing query parameters.
            args: Positional arguments.
            kwargs: Keyword arguments.

        Returns:
            Response: Redirects to the client application with a token, user_id, 
                      and role in the query string.
            HTTP 400 Response: If validation fails.
        """
        # Retrieve and merge form data
        form_data = request.session.get("form_data")
        if not form_data:
            return Response(
                {"error": "Form data is missing. Please complete the login process again."},
            )

        merged_form_data = {
            **request.GET.dict(),
            **form_data
        }

        input_serializer = self.InputSerializer(data=merged_form_data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        role = validated_data.get("role")
        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        # Handle errors
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        if not code or not state:
            return Response({"error": "Code and state are required."}, status=status.HTTP_400_BAD_REQUEST)

        # CSRF Check
        session_state = request.session.get("google_oauth2_state")
        if not session_state or state != session_state:
            return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

        del request.session["google_oauth2_state"]

        # Handle Google OAuth2 tokens
        google_login_flow = GoogleSdkLoginFlowService()
        google_tokens = google_login_flow.get_tokens(code=code, state=state)
        id_token_decoded = google_tokens.decode_id_token()
        user_email = id_token_decoded.get("email")

        if not user_email:
            return Response({"error": "Email not found in Google response."}, status=status.HTTP_400_BAD_REQUEST)

        # Role-based logic for finding the user
        user_model = None
        if role == "student":
            user_model = Student
        elif role == "professor":
            user_model = Professor
        elif role == "teacher_assistant":
            user_model = TeacherAssistant
        elif role == "sds_coordinator":
            user_model = SDSCoordinator
        else:
            return Response({"error": "Invalid role specified."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_model.objects.get(email=user_email)
        except user_model.DoesNotExist:
            return Response({"error": f"No {role} account found for this email."}, status=status.HTTP_404_NOT_FOUND)

        # Log the user in
        login(request, user)

        # Construct a query string for the redirect
        url_id = user.user_ptr_id
        user_base = User.objects.get(pk=user.pk)
        token, _ = Token.objects.get_or_create(user_id=user_base.id)

        redirect_url = f"http://localhost:5173/auth/callback?token={token.key}&user_id={url_id}&role={role}"

        return redirect(redirect_url)

class GoogleSdkLoginFlowService:
    """
    Defined Variables
    API_URI is the name of the API route in the usermanagement app that is called for callback, it invokes /callback
    The Google AUTH URLS are used for basic setup for th eGOogle Auth
    The Scopes are used to grab the google profiles and emails
    """
    API_URI = reverse_lazy("usermanagement:login/callback")

    # Two options are available: 'web', 'installed'
    GOOGLE_CLIENT_TYPE = "web"

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    # Add auth_provider_x509_cert_url if you want verification on JWTS such as ID tokens
    GOOGLE_AUTH_PROVIDER_CERT_URL = ""

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_sdk_login_get_credentials()

    def _get_redirect_uri(self):
        """
        Gets the redirect_uri for post-auth using API_URI and backend url
        """
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self):
        """
        Gets the Client JSON string using details from scopes and credentials
        Follow same format as client_secrets.json

        Returns:
            client_config: 
                Dict containing all necessary info for Google Auth0 Client
        """
        client_config = {
            self.GOOGLE_CLIENT_TYPE: {
                "client_id": self._credentials.client_id,
                "project_id": self._credentials.project_id,
                "auth_uri": self.GOOGLE_AUTH_URL,
                "token_uri": self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
                "auth_provider_x509_cert_url": self.GOOGLE_AUTH_PROVIDER_CERT_URL,
                "client_secret": self._credentials.client_secret,
                "redirect_uris": [self._get_redirect_uri()],
                "javascript_origins": [],
            }
        }
        return client_config

    # Reference:
    # https://developers.google.com/identity/protocols/oauth2/web-server#creatingclient
    def get_authorization_url(self):
        """
        Generates the Google OAuth2 authorization URL.

        This function builds the authorization URL using client credentials, 
        redirect URI, and requested scopes, allowing the user to authenticate 
        and grant access to their account.

        Returns:
            tuple: A tuple containing:
                - authorization_url (str): The URL to redirect the user to Google.
                - state (str): A unique state token for CSRF protection.
        """
        redirect_uri = self._get_redirect_uri()
        client_config = self._generate_client_config()

        google_oauth_flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=client_config, scopes=self.SCOPES
        )
        google_oauth_flow.redirect_uri = redirect_uri

        authorization_url, state = google_oauth_flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="select_account",
        )
        return authorization_url, state
    
    def get_tokens(self, *, code: str, state: str) -> GoogleAccessTokens:
        """
        Fetches Google OAuth2 tokens using an authorization code.

        This function exchanges the authorization code for an ID token and an 
        access token by making a POST request to Google's token endpoint.

        Parameters:
            code (str): The authorization code received from Google.

        Returns:
            GoogleAccessTokens: An object containing the ID token and access token.

        Raises:
            ApplicationError: If the token exchange fails.
        """
        redirect_uri = self._get_redirect_uri()
        client_config = self._generate_client_config()

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=client_config, scopes=self.SCOPES, state=state
        )
        flow.redirect_uri = redirect_uri
        access_credentials_payload = flow.fetch_token(code=code)

        if not access_credentials_payload:
            raise ApplicationError("Failed to obtain tokens from Google.")

        google_tokens = GoogleAccessTokens(
            id_token=access_credentials_payload["id_token"], 
            access_token=access_credentials_payload["access_token"]
        )

        return google_tokens
    
    def get_user_info(self, *, google_tokens: GoogleAccessTokens):
        """
        Retrieves user information from Google using an access token.

        This function makes an API call to Google's UserInfo endpoint to obtain 
        user details such as email and name.

        Parameters:
            google_tokens (GoogleAccessTokens): The access tokens obtained from Google.

        Returns:
            dict: A dictionary containing user information.

        Raises:
            ApplicationError: If the request to fetch user info fails.
        """
        access_token = google_tokens.access_token

        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={"access_token": access_token}
        )

        if not response.ok:
            raise ApplicationError("Failed to obtain user info from Google.")

        return response.json()    

@define
class GoogleSdkLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str
    
   
def google_sdk_login_get_credentials() -> GoogleSdkLoginCredentials:
    """
    Define SDK Login Credentials

    Returns:
        credentials:    
            Dict of the GOogleSDKLoginCredentials (client_id, client_secret, project_id), needed for auth
    """
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = settings.GOOGLE_OAUTH2_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_SECRET missing in env.")

    if not project_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_PROJECT_ID missing in env.")

    credentials = GoogleSdkLoginCredentials(
        client_id=client_id,
        client_secret=client_secret, 
        project_id=project_id
    )

    return credentials