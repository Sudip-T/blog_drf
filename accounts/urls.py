from django.urls import path
from .views import UserLoginSerializer, Logout, UserRegistrationView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/token/', UserLoginSerializer.as_view(), name='login_token'),
    path('logout/', Logout.as_view(), name='logout'),
]
