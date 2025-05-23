from django.urls import path
from .api import *
from .views import *
from .auth_login_api import *
from .auth_login_api import *
from .auth_signup_api import *
from .stream_api import *

app_name = "usermanagement"

urlpatterns = [
    path("students", get_students, name="get_students"),
    path("students/<int:user_id>", get_student, name="get_student"),
    path("students/add", add_student, name="add_student"),

    path("professors", get_professors, name="get_professors"),
    path("professors/<int:user_id>", get_professor, name="get_professor"),
    path("professors/add", add_professor, name="add_professor"),

    path("tas", get_tas, name="get_tas"),
    path("tas/<int:user_id>", get_ta, name="get_ta"),
    path("tas/add", add_ta, name="add_ta"),

    path("sdscoordinators", get_sdscoordinators, name="get_sdscoordinators"),
    path("sdscoordinators/<int:user_id>", get_sdscoordinator, name="get_sdscoordinator"),
    path("sdscoordinators/add", add_sds_coordinator, name="add_sds_coordinator"),

    # Auth Routes
    path("google-signup/redirect/", GoogleSignUpRedirectApi.as_view(), name="signup-redirect"),
    path("google-login/redirect/", GoogleLoginRedirectApi.as_view(), name="login-redirect"),
    path("signup/callback/", GoogleSignupAPI.as_view(), name="signup/callback"),
    path("login/callback/", GoogleLoginApi.as_view(), name="login/callback"),
    path('api-token-auth/', CustomAuthToken.as_view()),

    path('get-current-user', get_current_user, name="get_current_user"),
    path('user/token/<int:user_id>', get_token, name="get_token"),
    
    path('user/stream-token/<int:user_id>', get_stream_token, name="get_stream_token"),
    path('user/stream-admin/<int:user_id>', add_stream_permissions, name="add_stream_permissions")
]
