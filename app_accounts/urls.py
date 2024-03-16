from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app_accounts.apps import AppAccountsConfig

app_name = AppAccountsConfig.name

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
