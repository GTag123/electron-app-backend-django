from django.urls import path
from .views import (
    CreateUserAPIView,
    UserAuth,
    GetUserInfo,
    RefreshToken,
)
 
urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('login/', UserAuth.as_view()),
    path('info/', GetUserInfo.as_view()),
    path('token-refresh/', RefreshToken.as_view()),
]