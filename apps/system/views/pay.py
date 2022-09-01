from rest_framework import serializers
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from apps.system.models import Pay
from rest_framework.response import Response


class PaySerializer(ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"
        read_only_field = ["id"]
        ordering = ["date", ]


class PayViewSet(ModelViewSet):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    filterset_fields = ("date",)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.data["date"] == "":
            request.data["date"] = datetime.datetime.strftime(datetime.date.today(),"%Y-%m-%d")
        res = super().create(request, *args, **kwargs)
        return Response({"code": 200, "msg": "添加成功", "data": res.data})

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return Response({"code": 200, "msg": "编辑成功", "data": res.data})

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"code": 200, "msg": "删除成功", "data": []})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def monthly_payment(self, request):
        year = request.query_params["year"]
        month = request.query_params["month"]
        pay = Pay.objects.filter(date__month=month, date__year=year).order_by("-date")
        if pay:
            res = PaySerializer(pay, many=True)
            return Response({"code": 200, "msg": "success", "data": res.data})

        return Response({"code": 200, "msg": "暂无数据", "data": []})
