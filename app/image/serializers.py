from rest_framework import serializers
from .models import *
from django.apps import apps


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ["id", "title", "image", "uploaded_at"]

    def __init__(self, *args, **kwargs):
        model_name = kwargs.pop("model_name", None)
        if model_name:
            self.Meta.model = apps.get_model("image", model_name)
        super().__init__(*args, **kwargs)
