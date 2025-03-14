from rest_framework import serializers
from .models import CustomUser, Dish, Dish_Images

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class DishImageSerializer(serializers.Serializer):
    class Meta:
        model = Dish_Images
        fields = ['url']

class DishSerializer(serializers.ModelSerializer):
    photo = serializers.ListField(child=serializers.URLField(), write_only=True)  # Accepts list of URLs
    creator = serializers.PrimaryKeyRelatedField(read_only=True)  # Ensures creator is handled properly

    class Meta:
        model = Dish
        fields = ['name', 'category', 'ingredients', 'photo', 'creator']

    def create(self, validated_data):
        urls = validated_data.pop('photo', [])  # Extract URLs from request
        dish = Dish.objects.create(**validated_data)  # Create the dish instance

        # Create new Dish_Images objects for each URL
        image_objects = []
        for url in urls:
            image = Dish_Images.objects.create(name=f"Image for {dish.name}", url=url)
            image_objects.append(image)

        # Assign images to the dish
        dish.photo.set(image_objects)
        return dish