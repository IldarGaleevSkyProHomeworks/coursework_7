from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField


class StartNotifySerializer(serializers.Serializer):
    timezone = TimeZoneSerializerField(use_pytz=False)
