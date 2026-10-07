from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    # Trainer's full name
    name = models.CharField(max_length=100)

    # What the trainer specializes in
    specialization = models.CharField(max_length=100)

    # Number of years of experience
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        # This is what StringRelatedField will show
        return self.name


class GymClass(models.Model):
    # Name of the gym class
    title = models.CharField(max_length=100)

    # One trainer can have many gym classes
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='gym_classes'
    )

    # Date of the class
    date = models.DateField()

    # Duration in minutes
    duration = models.PositiveIntegerField()

    # Maximum number of people
    max_participants = models.PositiveIntegerField()

    # Number of already booked places
    booked_places = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='gym_classes',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Booking(models.Model):
    gym_class = models.ForeignKey(
        GymClass,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.client_name} - {self.gym_class.title}'