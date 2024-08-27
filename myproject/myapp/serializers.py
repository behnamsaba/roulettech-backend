from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Recipe, SavedRecipe



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('recipe_id', 'title')


class SavedRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        source='recipe',
        write_only=True
    )

    class Meta:
        model = SavedRecipe
        fields = ('user', 'recipe', 'saved_on', 'recipe_id')

    def create(self, validated_data):
        saved_recipe = SavedRecipe.objects.create(
            user=self.context['request'].user,
            recipe=validated_data['recipe']
        )
        return saved_recipe
    
class SavedRecipeListSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = SavedRecipe
        fields = ('recipe', 'saved_on')