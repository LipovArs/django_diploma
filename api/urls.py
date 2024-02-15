from django.urls import path
from . import views

urlpatterns = [

    path('sign_up/', views.sign_up),
    path('login/', views.login),
    path('logout/', views.logout),

    path('tasks/', views.TaskListCreate.as_view()),
    path('task/<int:pk>/', views.TaskRetrieveUpdate.as_view()),
    path('task/<int:pk>/assign/', views.BecomeAssigner.as_view()),
    path('task/<int:pk>/<str:direction>/move/', views.TaskMove.as_view()),
    path('tasks/<str:status_id>', views.TaskByStatus.as_view()),

    path('task/<int:pk>/del', views.TaskDelete.as_view()),
    path('task/<int:pk>/<int:user_id>/appoint', views.AppointAssigner.as_view())
]
