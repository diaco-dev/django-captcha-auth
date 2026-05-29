from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import RegisterView, CustomLoginView, VerifyCodeView, RegisterCodeView, VerifyCode2View

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', CustomLoginView.as_view(), name='log_in'),
    path("register-send-code/", RegisterCodeView.as_view(), name="register_code"),
    path("verify/", VerifyCodeView.as_view(), name="verify_code"),
    path("verify2/", VerifyCode2View.as_view(), name="verify"),
]