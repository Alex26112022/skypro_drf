from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer
