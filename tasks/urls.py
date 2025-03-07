from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
    path('api/tasks/', views.get_tasks_json, name='get_tasks_json'),
    path('api/counts/', views.task_counts, name='task_counts'),
    path('signup/', views.signup, name='signup'),  # New signup path
]