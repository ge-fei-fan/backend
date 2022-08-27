from django.contrib.auth import login
from django.contrib import auth
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.translation import gettext_lazy as _
from apps.user.models import Users
from rest_framework import serializers

class LoginSerializer(TokenObtainPairSerializer):

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    default_error_messages = {"no_active_account": _("账号/密码错误")}
    def validate(self, attrs):
        data = super().validate(attrs)
        userinfo = {
            "username": self.user.username,
            "avatar": self.user.avatar
        }
        data["userinfo"] = userinfo
        return {"code": 200, "msg": "请求成功", "data": data}


class LoginView(TokenObtainPairView):

    serializer_class = LoginSerializer


class ApiLoginSerializer(ModelSerializer):
    """接口文档登录-序列化器"""

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Users
        fields = ["username", "password"]




class ApiLogin(APIView):
    """接口文档的登录接口"""

    serializer_class = ApiLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user_obj = auth.authenticate(
            request,
            username=username,
            password=password,
        )
        if user_obj:
            login(request, user_obj)
            return redirect("/")
        else:
            return Response({"code": 400, "msg": "账号/密码错误", "data": None})
