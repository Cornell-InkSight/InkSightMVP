from django.shortcuts import redirect
import requests
from django.conf import settings
from django.urls import reverse_lazy
from rest_framework import serializers, status
from rest_framework.response import Response
from django.conf import settings
import google_auth_oauthlib.flow
from attrs import define
from typing import Dict, Any
from usermanagement.models import *
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .auth_helper_classes import PublicApi, CustomAuthToken, GoogleAccessTokens
from django.core.exceptions import ImproperlyConfigured

class GoogleSignUpRedirectApi(PublicApi):
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
        year = request.GET.get("year")
        disability = request.GET.get("disability")
        sds_coordinator_access_code = request.GET.get("sds_coordinator_access_code")
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
            if not all([school_id, year, disability, sds_coordinator_access_code]):
                return Response(
                    {"error": "All fields are required for students (school_id, year, disability, sds_coordinator_access_code)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.session["form_data"] = {
                "role": role,
                "school_id": school_id,
                "year": year,
                "disability": disability,
                "sds_coordinator_access_code": sds_coordinator_access_code,
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


        google_sign_in_flow = GoogleSdkSignupFlowService()
        authorization_url, state = google_sign_in_flow.get_authorization_url()

        # Store the OAuth state in session
        request.session["google_oauth2_state"] = state

        return redirect(authorization_url)


class GoogleSignupAPI(PublicApi):
    """Serializer For The Input --> data is validated"""
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=True)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=True)
        school_id = serializers.CharField(required=True)
        year = serializers.IntegerField(required=False)
        disability = serializers.CharField(required=False)
        sds_coordinator_access_code = serializers.CharField(required=False)
        title = serializers.CharField(required=False)
        professor_id = serializers.CharField(required=False)
        position = serializers.CharField(required=False)
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
        form_data = request.session.get("form_data")
        if not form_data:
            return Response(
                {"error": "Form data is missing. Please complete the login process again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Merge the Form Data (which is drawn from the HTML) and GET data which is the google auth
        merged_form_data = {
            **request.GET.dict(),
            **form_data
        }

        # Check serializer to ensure data validity
        input_serializer = self.InputSerializer(data=merged_form_data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        # A Bunch of gets to get the data from the serializer, now that we have verifiedit
        school_id = validated_data.get("school_id")
        year = validated_data.get("year")
        disability = validated_data.get("disability")
        role = validated_data.get("role")
        sds_coordinator_access_code = validated_data.get("sds_coordinator_access_code")
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
        google_login_flow = GoogleSdkSignupFlowService()
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
                sds_coordinator = SDSCoordinator.objects.get(access_code=sds_coordinator_access_code)
            except SDSCoordinator.DoesNotExist:
                e = "SDSCoordinator with access code {sds_coordinator_access_code} does not exist."
                return redirect(f"{settings.FRONTEND_URL}/signin?error={str(e)}")


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

        try:
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

            # The User of the ID for redirect
            url_id = user.user_ptr_id

            redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={token.key}&user_id={url_id}&role={role}"

            return redirect(redirect_url)
        except Exception as e:
            return redirect(f"{settings.FRONTEND_URL}/signin?error={str(e)}")

class GoogleSdkSignupFlowService:
    """
    Defined Variables
    API_URI is the name of the API route in the usermanagement app that is called for callback, it invokes /callback
    The Google AUTH URLS are used for basic setup for th eGOogle Auth
    The Scopes are used to grab the google profiles and emails
    """
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
        print("Authorization URL:", authorization_url)
        print("State:", state)

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

