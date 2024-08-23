from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from lms.models import Course
from users.models import User, Payments, StripePayment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentsSerializer, \
    UserDetailSerializer, StripePaymentSerializer
from users.services import create_stripe_price, create_stripe_session


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
        obj_user = User.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        print(obj_user)
        print(user)
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
        amount = Course.objects.get(pk=payment.course_id).price
        price = create_stripe_price(amount)
        session_id, link_payment = create_stripe_session(price)
        payment.session_id = session_id
        payment.link_payment = link_payment
        payment.save()
