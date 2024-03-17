from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app_accounts.apps import AppAccountsConfig
from app_accounts.view import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

app_name = AppAccountsConfig.name

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
