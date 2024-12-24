from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),  # Chatbot home page
    path('login/', views.login, name='login'),     # Login page
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),  # Custom logout view
]
