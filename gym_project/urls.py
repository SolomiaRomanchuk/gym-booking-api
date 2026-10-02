from django.contrib import admin
from django.urls import path

from gym import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/classes/',
        views.GymClassListView.as_view(),
        name='gym_class_list'
    ),

    path(
        'api/classes/<int:pk>/',
        views.GymClassDetailView.as_view(),
        name='gym_class_detail'
    ),

    path(
        'api/trainers/',
        views.TrainerListView.as_view(),
        name='trainer_list'
    ),
]