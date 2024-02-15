from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'board'

login_url='board:registration'

urlpatterns = [
    path('', login_required(views.home_view, login_url=login_url), name='home'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('create_task/', login_required(views.TaskCreateView.as_view(), login_url=login_url), name='create_task'),
    path('update_task/<int:pk>/', login_required(views.TaskUpdateView.as_view(), login_url=login_url), name='update_task'),
    path('change_status/<int:pk>/<str:direction>/', login_required(views.change_status, login_url=login_url), name='change_status'),
    path('become_assigner/<int:pk>/', login_required(views.become_assigner, login_url=login_url), name='become_assigner'),
    path('delete_task/<int:pk>/', login_required(views.TaskDeleteView.as_view(), login_url=login_url), name='delete_task'),
    path('appoint_assigner/<int:pk>', login_required(views.appoint_assigner, login_url=login_url), name='appoint_assigner'),
    path('check_status/<str:status_id>', login_required(views.check_status, login_url=login_url), name='check_status'),
]
