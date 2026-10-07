from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import models
from .models import Trainer, GymClass, Booking
from .serializers import (
    TrainerSerializer,
    GymClassSerializer,
    BookingSerializer
)
from .permissions import IsOwnerOrReadOnly


class TrainerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

    search_fields = ['name', 'specialization']
    ordering_fields = ['name', 'experience_years']
    ordering = ['id']


class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.select_related(
        'trainer',
        'owner'
    ).all()

    serializer_class = GymClassSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    filterset_fields = ['trainer', 'date']

    search_fields = [
        'title',
        'trainer__name'
    ]

    ordering_fields = [
        'date',
        'duration',
        'max_participants'
    ]

    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def available(self, request):
        classes = self.get_queryset().filter(
            booked_places__lt=models.F('max_participants')
        )

        serializer = self.get_serializer(
            classes,
            many=True
        )

        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related(
        'gym_class',
        'owner'
    ).all()

    serializer_class = BookingSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    filterset_fields = ['gym_class']

    search_fields = [
        'client_name',
        'client_email'
    ]

    ordering_fields = ['client_name']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)