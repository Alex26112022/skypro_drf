from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from users.apps import UsersConfig

from users.views import UserListAPIView, UserCreateAPIView, UserDestroyAPIView, \
    UserUpdateAPIView, UserRetrieveAPIView, PaymentsListAPIView, \
    StripePaymentCreateAPIView, StripePaymentRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments_list/', PaymentsListAPIView.as_view(),
         name='payments_list'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(),
         name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(),
         name='user_delete'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
         name='login'),
    path('refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)),
         name='refresh'),
    path('stripe-payment/', StripePaymentCreateAPIView.as_view(),
         name='stripe_payment_create'),
    path('stripe-payment/check-status/',
         StripePaymentRetrieveAPIView.as_view(), name='stripe_payment_status')
]
