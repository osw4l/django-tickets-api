from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ticket, TicketImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'get_full_name'
        )


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Ticket
        fields = (
            'uuid',
            'user',
            'total_images',
            'created_at',
            'updated_at',
            'status'
        )
        read_only_fields = ('status',)


class TicketImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketImage
        fields = (
            'uuid',
            'image',
            'status'
        )


class TicketDetailSerializer(serializers.ModelSerializer):
    images = TicketImageSerializer(many=True, read_only=True)

    class Meta(TicketSerializer.Meta):
        fields = TicketSerializer.Meta.fields + (
           'images',
        )

