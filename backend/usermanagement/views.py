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
    


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class GoogleSignUpRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
        role = request.GET.get("role")
        year = request.GET.get("year")
        disability = request.GET.get("disability")
        sds_coordinator_id = request.GET.get("sds_coordinator_id")
        title = request.GET.get("title")
        school_id = request.GET.get("school_id")
        professor_id = request.GET.get("professor_id")
        position = request.GET.get("position")

        if not role:
            return Response(
                {"error": "Role is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validation based on the role
        if role == "student":
            if not all([school_id, year, disability, sds_coordinator_id]):
                return Response(
                    {"error": "All fields are required for students (school_id, year, disability, sds_coordinator_id)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.session["form_data"] = {
                "role": role,
                "school_id": school_id,
                "year": year,
                "disability": disability,
                "sds_coordinator_id": sds_coordinator_id,
            }
        elif role == "professor":
            if not all([school_id, title]):
                return Response(
                    {"error": "All fields are required for professors (school_id, title)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.session["form_data"] = {
                "role": role,
                "school_id": school_id,
                "title": title,
            }
        elif role == "teacher_assistant":
            if not all([school_id, professor_id]):
                return Response(
                    {"error": "All fields are required for teacher assistants (school_id, professor_id)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.session["form_data"] = {
                "role": role,
                "school_id": school_id,
                "professor_id": professor_id,
            }
        elif role == "sds_coordinator":
            if not all([school_id, position]):
                return Response(
                    {"error": "All fields are required for SDS Coordinators (school_id, position)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.session["form_data"] = {
                "role": role,
                "school_id": school_id,
                "position": position,
            }
        else:
            return Response(
                {"error": "Invalid role provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        google_login_flow = GoogleSdkSignupFlowService()
        authorization_url, state = google_login_flow.get_authorization_url()

        # Store the OAuth state in session
        request.session["google_oauth2_state"] = state

        return redirect(authorization_url)

class GoogleLoginRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
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

class GoogleRawLoginFlowService:
    API_URI = reverse_lazy("usermanagement:callback")

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_raw_login_get_credentials()

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state
    
    def get_tokens(self, *, code: str) -> GoogleAccessTokens:
        redirect_uri = self._get_redirect_uri()

        data = {
            "code": code,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            raise ApplicationError("Failed to obtain access token from Google.")

        tokens = response.json()
        google_tokens = GoogleAccessTokens(
            id_token=tokens["id_token"],
            access_token=tokens["access_token"]
        )

        return google_tokens


class GoogleSignInAPI(PublicApi):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=True)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=True)
        school_id = serializers.CharField(required=True)
        year = serializers.IntegerField(required=False)
        disability = serializers.CharField(required=False)
        sds_coordinator_id = serializers.CharField(required=False)
        title = serializers.CharField(required=False)
        professor_id = serializers.CharField(required=False)
        position = serializers.CharField(required=False)
        role = serializers.CharField(required=True)

    def get(self, request, *args, **kwargs):
        # Retrieve and merge form data
        form_data = request.session.get("form_data")
        if not form_data:
            return Response(
                {"error": "Form data is missing. Please complete the login process again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        merged_form_data = {
            **request.GET.dict(),
            **form_data
        }

        input_serializer = self.InputSerializer(data=merged_form_data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        school_id = validated_data.get("school_id")
        year = validated_data.get("year")
        disability = validated_data.get("disability")
        role = validated_data.get("role")
        sds_coordinator_id = validated_data.get("sds_coordinator_id")
        title = validated_data.get("title")
        professor_id = validated_data.get("professor_id")
        position = validated_data.get("position")
        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        # Handle errors
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        if not code or not state:
            return Response({"error": "Code and state are required."}, status=status.HTTP_400_BAD_REQUEST)

        session_state = request.session.get("google_oauth2_state")
        if not session_state or state != session_state:
            return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

        del request.session["google_oauth2_state"]

        # Handle Google OAuth2 tokens
        google_login_flow = GoogleSdkLoginFlowService()
        google_tokens = google_login_flow.get_tokens(code=code, state=state)
        id_token_decoded = google_tokens.decode_id_token()
        user_email = id_token_decoded.get("email")
        first_name = id_token_decoded.get("given_name", "")
        last_name = id_token_decoded.get("family_name", "")

        if not user_email:
            return Response({"error": "Email not found in Google response."}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create school
        school, _ = School.objects.get_or_create(id=school_id)

        # Role-based logic
        if role == "student":
            try:
                sds_coordinator = SDSCoordinator.objects.get(access_code=sds_coordinator_id)
            except SDSCoordinator.DoesNotExist:
                return Response(
                    {"error": f"SDSCoordinator with access code {sds_coordinator_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_model = Student
            user_defaults = {
                "name": f"{first_name} {last_name}",
                "school": school,
                "year": year,
                "disability": disability,
                "sds_coordinator": sds_coordinator,
            }

        elif role == "professor":
            user_model = Professor
            user_defaults = {
                "name": f"{first_name} {last_name}",
                "school": school,
                "title": title,
            }

        elif role == "teacher_assistant":
            try:
                assigned_professor = Professor.objects.get(pk=professor_id)
            except Professor.DoesNotExist:
                return Response(
                    {"error": f"Professor with ID {professor_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_model = TeacherAssistant
            user_defaults = {
                "name": f"{first_name} {last_name}",
                "school": school,
                "assigned_professor": assigned_professor,
            }

        elif role == "sds_coordinator":
            user_model = SDSCoordinator
            user_defaults = {
                "name": f"{first_name} {last_name}",
                "school": school,
                "position": position,
            }

        else:
            return Response({"error": "Invalid role specified."}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create user
        user, created = user_model.objects.get_or_create(
            email=user_email,
            defaults=user_defaults
        )
        user_base = User.objects.get(pk=user.pk)
        token, _ = Token.objects.get_or_create(user_id=user_base.id)

        if created:
            print(f"Created new {role}: {user.name}")
        else:
            print(f"{role.capitalize()} {user.name} already exists.")

        # Log the user in
        login(request, user)

        # Response data
        # Construct a query string for the redirect
        url_id = user.user_ptr_id

        redirect_url = f"http://localhost:5173/auth/callback?token={token.key}&user_id={url_id}&role={role}"

        return redirect(redirect_url)


class GoogleLoginApi(PublicApi):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=True)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=True)
        role = serializers.CharField(required=True)

    def get(self, request, *args, **kwargs):
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

    

@define
class GoogleSdkLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str
    
   
def google_sdk_login_get_credentials() -> GoogleSdkLoginCredentials:
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


class GoogleSdkLoginFlowService:
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
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self):
        # This follows the structure of the official "client_secret.json" file
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
        access_token = google_tokens.access_token

        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={"access_token": access_token}
        )

        if not response.ok:
            raise ApplicationError("Failed to obtain user info from Google.")

        return response.json()
        

class GoogleSdkSignupFlowService:
    API_URI = reverse_lazy("usermanagement:signup/callback")

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
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def _generate_client_config(self):
        # This follows the structure of the official "client_secret.json" file
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
        access_token = google_tokens.access_token

        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={"access_token": access_token}
        )

        if not response.ok:
            raise ApplicationError("Failed to obtain user info from Google.")

        return response.json()
        


class CustomAuthToken(ObtainAuthToken):
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
