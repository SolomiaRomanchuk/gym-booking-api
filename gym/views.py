from rest_framework import generics

from .models import Trainer, GymClass
from .serializers import TrainerSerializer, GymClassSerializer


class GymClassListView(generics.ListAPIView):
    serializer_class = GymClassSerializer

    def get_queryset(self):
        queryset = GymClass.objects.all()

        trainer = self.request.query_params.get('trainer')

        if trainer:
            queryset = queryset.filter(trainer_id=trainer)

        return queryset


class GymClassDetailView(generics.RetrieveAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassSerializer


class TrainerListView(generics.ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
