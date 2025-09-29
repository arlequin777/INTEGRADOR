from django.urls import path
from .views import CustomTokenObtainPairView , UserRoleUpdateView, UserCreateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("users/", UserCreateView.as_view(), name="user-create"),
    path('users/<int:pk>/roles/', UserRoleUpdateView.as_view(), name="user-role-update"),
 ]
