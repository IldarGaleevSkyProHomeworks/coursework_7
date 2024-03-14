from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app_telegrambot.tasks import process_telegram_webhook_task


@swagger_auto_schema(method='post', auto_schema=None)
@api_view(['POST'])
@permission_classes([AllowAny])
def telegram_webhook(request):
    process_telegram_webhook_task.delay(request.data)
    return Response({'success': True})
