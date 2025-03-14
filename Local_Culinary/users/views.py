from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Dish
from .serializers import LoginSerializer, UserSerializer, DishSerializer

User = get_user_model()

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = user.tokens()
        result = {
            'username': serializer.data['username'], 
            'refresh': refresh['refresh'], 
            'access': refresh['acsses']
        }
        return Response(result, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Try to find user
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({'error': "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check password correctly
        if not check_password(password, user.password):  
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens
        refresh = user.tokens()
        result = {
            'username': user.username,
            'refresh': refresh['refresh'],
            'acsses': refresh['acsses']
        }
        return Response(result, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        # Access the authenticated user's details
        user = request.user
        return Response({"username": user.username, "email": user.email})


class DishView(CreateAPIView, APIView):
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dish = serializer.save(creator=request.user)
        result = {
            'dish_name': dish.name,
            'category': dish.category,
            'ingredients': dish.ingredients,
            'creator': dish.creator.username,
            'photos': [photo.url for photo in dish.photo.all()]
        }
        return Response(result, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        dish_id = kwargs.get('pk')
        try:
            dish = Dish.objects.get(id=dish_id, creator=request.user)
            dish.delete()
            return Response({"message": "Dish successfully deleted"}, status=status.HTTP_200_OK)
        except Dish.DoesNotExist:
            return Response({"error": "Dish not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        dish_id = kwargs.get('pk')
        try:
            dish = Dish.objects.get(id=dish_id, creator=request.user)
        except Dish.DoesNotExist:
            return Response({"error": "Dish not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DishSerializer(dish, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Dish updated successfully", "dish": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)