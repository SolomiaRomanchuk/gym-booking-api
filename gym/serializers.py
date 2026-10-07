from rest_framework import serializers
from .models import Trainer, GymClass, Booking


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
    trainer_name = serializers.CharField(
        source='trainer.name',
        read_only=True
    )

    owner = serializers.ReadOnlyField(
        source='owner.username'
    )

    available_places = serializers.SerializerMethodField()

    class Meta:
        model = GymClass
        fields = [
            'id',
            'title',
            'trainer',
            'trainer_name',
            'date',
            'duration',
            'max_participants',
            'booked_places',
            'available_places',
            'owner'
        ]

    def get_available_places(self, obj):
        return obj.max_participants - obj.booked_places

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Duration must be greater than 0.'
            )

        return value

    def validate(self, data):
        max_participants = data.get(
            'max_participants',
            getattr(self.instance, 'max_participants', None)
        )

        booked_places = data.get(
            'booked_places',
            getattr(self.instance, 'booked_places', 0)
        )

        if (
            max_participants is not None
            and booked_places > max_participants
        ):
            raise serializers.ValidationError(
                'Booked places cannot be greater than maximum participants.'
            )

        return data


class BookingSerializer(serializers.ModelSerializer):
    gym_class_title = serializers.CharField(
        source='gym_class.title',
        read_only=True
    )

    owner = serializers.ReadOnlyField(
        source='owner.username'
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'gym_class',
            'gym_class_title',
            'client_name',
            'client_email',
            'owner'
        ]