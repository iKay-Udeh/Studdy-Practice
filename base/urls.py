from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('update-comment/<str:pk>/', views.updateComment, name='update-comment'),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topics, name='topic'),
    path('activities/', views.activities, name='activity'),
]
