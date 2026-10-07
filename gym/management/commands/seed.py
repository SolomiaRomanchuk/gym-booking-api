from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from gym.models import Trainer, GymClass, Booking


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):

        if Trainer.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    'Data already exists, skipping.'
                )
            )
            return

        user, _ = User.objects.get_or_create(
            username='demo'
        )

        trainer1 = Trainer.objects.create(
            name='Anna Smith',
            specialization='Yoga',
            experience_years=5
        )

        trainer2 = Trainer.objects.create(
            name='John Brown',
            specialization='Fitness',
            experience_years=8
        )

        gym_class1 = GymClass.objects.create(
            title='Morning Yoga',
            trainer=trainer1,
            date=date(2026, 10, 10),
            duration=60,
            max_participants=15,
            booked_places=8,
            owner=user
        )

        GymClass.objects.create(
            title='Functional Training',
            trainer=trainer2,
            date=date(2026, 10, 11),
            duration=45,
            max_participants=20,
            booked_places=10,
            owner=user
        )

        Booking.objects.create(
            gym_class=gym_class1,
            client_name='Test Client',
            client_email='client@example.com',
            owner=user
        )

        self.stdout.write(
            self.style.SUCCESS('Done.')
        )