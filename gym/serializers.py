from rest_framework import serializers
from .models import Trainer, GymClass


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = [
            'id',
            'name',
            'specialization',
            'experience_years'
        ]


class GymClassSerializer(serializers.ModelSerializer):
    # Shows trainer's name instead of trainer's ID
    trainer = serializers.StringRelatedField()

    # Calculated field
    available_places = serializers.SerializerMethodField()

    class Meta:
        model = GymClass
        fields = [
            'id',
            'title',
            'trainer',
            'date',
            'duration',
            'max_participants',
            'booked_places',
            'available_places'
        ]

    def get_available_places(self, obj):
        return obj.max_participants - obj.booked_places