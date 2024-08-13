from django.urls import path

from users.apps import UsersConfig

from users.views import UserListAPIView, UserCreateAPIView, UserDestroyAPIView, \
    UserUpdateAPIView, UserRetrieveAPIView, PaymentsListAPIView

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
]
