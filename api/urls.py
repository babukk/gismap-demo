from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api import views

app_name = 'api'

router = DefaultRouter()

router.register('checkpoint', views.CheckpointViewSet)
router.register('task', views.TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('tasks/', views.ActiveTaskList.as_view(), name='active_task_list'),
]
