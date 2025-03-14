from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProtectedView, DishView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('dish/create/', DishView.as_view(), name='create_dish'),
    path('dish/<int:pk>/', DishView.as_view(), name='delete_dish'),
    path('dish/<int:pk>/', DishView.as_view(), name='update_dish'),
    path('dish/<int:pk>', DishView.as_view(), name='read_dish'),
    path('dishes/', DishView.as_view(), name='get_every_dish')
]