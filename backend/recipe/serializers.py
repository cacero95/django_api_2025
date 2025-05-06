from rest_framework import serializers
from .models import Recipe
from helpers.validate_image import format_image
import os

class RecipeSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source='category.name')
    created_date = serializers.DateTimeField(format='%d/%m/%Y')
    image = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    # user = serializers.ReadOnlyField(source='user.first_name')
    class Meta:
        model = Recipe
        fields = (
            'id','name', 'slug', 'description', 'time',
            'image', 'created_date', 'category',
            'category_id', 'user_id', 'user'
        )

    def get_user(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_image(self, obj):
        return format_image(obj.image)