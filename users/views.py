from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from pytz import timezone
from rest_framework import filters

from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from config.settings import TIME_ZONE
from lms.models import Course
from users.models import User, Payments, StripePayment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentsSerializer, \
    UserDetailSerializer, StripePaymentSerializer, StatusPaymentSerializer, \
    StatusPaymentSwaggerSerializer
from users.services import create_stripe_price, create_stripe_session, \
    get_status_payment, create_stripe_product

tz = timezone(TIME_ZONE)


class UserListAPIView(ListAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        obj_user = User.objects.get(pk=self.kwargs.get('pk'))
        user = self.request.user
        if user.is_superuser or user == obj_user:
            return UserDetailSerializer
        else:
            return UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsUser]

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        if self.request.data.get('password') is not None:
            user.set_password(user.password)
        user.save()


class UserDestroyAPIView(DestroyAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsUser]


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering = ['date_of_payment']


class StripePaymentCreateAPIView(CreateAPIView):
    queryset = StripePayment.objects.all()
    serializer_class = StripePaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course = Course.objects.get(pk=payment.course_id)
        product = create_stripe_product(course.title, course.description)
        price = create_stripe_price(course.price, product)
        session_id, link_payment = create_stripe_session(price)
        payment.session_id = session_id
        payment.link_payment = link_payment
        payment.save()


@method_decorator(name='post', decorator=swagger_auto_schema(
    request_body=StatusPaymentSwaggerSerializer,
    responses={'201': 'Ok', 'Example Value': '{"status": "string"}'}, ))
class StripePaymentRetrieveAPIView(APIView):
    queryset = StripePayment.objects.all()
    serializer_class = StatusPaymentSerializer

    def post(self, request, *args, **kwargs):
        payment = StripePayment.objects.get(
            session_id=self.request.data.get('session_id'))
        payment.status_payment = get_status_payment(payment.session_id)
        status = f'{payment.status_payment}'
        payment.save()
        return Response({"status": status})


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        now = datetime.now(tz)
        user = get_object_or_404(User, email=request.data.get('email'))
        user.last_login = now
        user.save()
        return super().post(request, *args, **kwargs)
