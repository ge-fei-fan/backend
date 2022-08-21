from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.system.models import FileList


class FileSerializer(ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        return 'media/' + str(instance.url)


    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):

        validated_data["name"] = str(self.initial_data.get("file"))
        validated_data['url'] = self.initial_data.get('file')
        return super().create(validated_data)


class FileViewSet(ModelViewSet):

    queryset = FileList.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ("name",)
