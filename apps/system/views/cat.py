import datetime

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from apps.system.models import Cat, Weight


class CatSerializer(ModelSerializer):

    avatar = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Cat
        fields = "__all__"
        read_only_field = ["id"]

class WeightSerializer(ModelSerializer):


    class Meta:
        model = Weight
        fields = "__all__"
        read_only_field = ["id"]


class CatViewSet(ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filterset_fields = ("id",)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"code": 200, "msg": "新增成功", "data": serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"code": 200, "msg": "更新成功", "data": serializer.data})


class WeightViewset(ModelViewSet):

    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    filterset_fields = ("id", "cat", "date")
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.data["date"] == "":
            request.data["date"] = datetime.datetime.strftime(datetime.date.today(),"%Y-%m-%d")
        wg = Weight.objects.filter(cat=request.data["cat"], date__gte=request.data["date"], date__lte=request.data["date"])
        if wg:
            wg.update(**request.data)
            return Response({"code": 200, "msg": "更新成功"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"code": 200, "msg": "新增成功", "data": serializer.data})

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return Response({"code": 200, "msg": "修改成功", "data": res.data})

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"code": 200, "msg": "删除成功", "data": None})







