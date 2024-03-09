from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from app_telegrambot.services import process_webhook
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def telegram_webhook(request):
    process_webhook(request.data)
    return Response({'success': True})
