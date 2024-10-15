from django.urls import path
from customauth.api.views import LoginView,SignupView,DeleteUserView

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('deleteuser/<int:pk>/',DeleteUserView.as_view(),name='delete-user'),
]