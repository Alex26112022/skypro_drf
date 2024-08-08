from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from users.models import Payments


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'phone', 'country', 'avatar')


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
