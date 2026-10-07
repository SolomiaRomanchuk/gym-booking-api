from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gym import views


router = DefaultRouter()

router.register(
    'classes',
    views.GymClassViewSet,
    basename='gym-class'
)

router.register(
    'trainers',
    views.TrainerViewSet,
    basename='trainer'
)

router.register(
    'bookings',
    views.BookingViewSet,
    basename='booking'
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/',
        include(router.urls)
    ),

    path(
        'api-auth/',
        include('rest_framework.urls')
    ),
]