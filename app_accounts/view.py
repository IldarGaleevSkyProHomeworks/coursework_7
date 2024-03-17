from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app_accounts.pagination import AppAccountsPagination
from app_accounts.permissions import IsAnonCreate, IsOwner
from app_accounts.serializers import UserPublicSerializer, UserSerializer
from app_accounts.serializers.user_public_serializer import UserEditSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,

):
    """
            create:
            Регистрация нового пользователя.

            retrieve:
            Информация о пользователе.

            list:
            Возвращает список пользователей.

            partial_update:
            Править часть информации о пользователе.

            destroy:
            Удалить пользователя

        """

    serializer_class = UserPublicSerializer
    queryset = User.objects.all()
    permission_classes = (IsAnonCreate | IsAuthenticated,)
    pagination_class = AppAccountsPagination
    http_method_names = ['patch', 'get', 'post', 'delete']

    def get_permissions(self):
        match self.action:
            case 'create':
                self.permission_classes = (IsAnonCreate,)
            case 'update' | 'partial_update':
                self.permission_classes = (IsOwner | IsAdminUser,)
            case 'destroy':
                self.permission_classes = (IsAdminUser,)
            case _:
                pass

        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        is_swagger = getattr(self, 'swagger_fake_view', False)

        if is_swagger and self.action == 'create':
            return UserSerializer

        if self.action in ('update', 'partial_update'):
            return UserEditSerializer
        else:
            return UserPublicSerializer
