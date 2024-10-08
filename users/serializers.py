from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from users.models import Payments, StripePayment


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'phone', 'country', 'avatar')


class UserDetailSerializer(ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'payments', 'email', 'password', 'first_name', 'last_name',
            'phone', 'country', 'avatar', 'is_active', 'date_joined',
            'last_login', 'groups')


class StripePaymentSerializer(ModelSerializer):
    class Meta:
        model = StripePayment
        fields = '__all__'


class StatusPaymentSerializer(ModelSerializer):
    class Meta:
        model = StripePayment
        fields = ('session_id', 'status_payment',)


class StatusPaymentSwaggerSerializer(ModelSerializer):
    class Meta:
        model = StripePayment
        fields = ('session_id',)
