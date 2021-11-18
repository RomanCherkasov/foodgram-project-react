from django.db import models
from django.db.models import fields
from recipes.models import Ingredients
from rest_framework import serializers


class IngidientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit',
        )