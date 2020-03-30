from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    to = serializers.CharField()
    message = serializers.CharField()
