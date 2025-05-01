from rest_framework import serializers
from .models import Recipe
from helpers.validate_image import format_image
import os

class RecipeSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source='category.name')
    created_date = serializers.DateTimeField(format='%d/%m/%Y')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id','name', 'slug', 'description', 'time', 'image', 'created_date', 'category', 'category_id')

    def get_image(self, obj):
        return format_image(obj.image)