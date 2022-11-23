from django.urls import path, include
from . import views
from .views import RegistrationAPIView


urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('get/user/<int:id>/', views.get_user),
]
