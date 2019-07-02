from django.urls import path
from .views import CreateUserAPIView, UserAuth
 
urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('login/', UserAuth.as_view()),
]