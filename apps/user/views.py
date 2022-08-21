from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.translation import gettext_lazy as _
from apps.user.models import Users

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



