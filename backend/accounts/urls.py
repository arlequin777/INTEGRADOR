from django.urls import path
from .views import CustomTokenObtainPairView , UserCreateView , UserUpdateRoleView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("users", UserCreateView.as_view(), name="user-create"),
    path("users/<uuid:id>/roles", UserUpdateRoleView.as_view(), name="user-update-role"),
]
