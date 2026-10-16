
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Trainer, GymClass, Booking


User = get_user_model()


class GymAPITests(TestCase):

    def setUp(self):
        # Створюємо двох користувачів для перевірки прав доступу
        self.user1 = User.objects.create_user(
            username="user1",
            password="TestPassword123!"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="TestPassword456!"
        )

        # Створюємо клієнт для API-запитів
        self.client = APIClient()

        # Створюємо тестового тренера
        self.trainer = Trainer.objects.create(
            name="Anna Smith",
            specialization="Yoga",
            experience_years=5
        )

        # Створюємо заняття, власником якого є user1
        self.gym_class = GymClass.objects.create(
            title="Morning Yoga",
            trainer=self.trainer,
            date=date.today() + timedelta(days=7),
            duration=60,
            max_participants=10,
            booked_places=2,
            owner=self.user1
        )

        # Створюємо бронювання, власником якого є user1
        self.booking = Booking.objects.create(
            gym_class=self.gym_class,
            client_name="John Smith",
            client_email="john@example.com",
            owner=self.user1
        )

    def authenticate(self, user):
        # Авторизуємо користувача в тестовому клієнті
        self.client.force_authenticate(user=user)

    def test_login_success(self):
        # Перевіряємо вхід із правильним паролем
        response = self.client.post(
            "/api/token/",
            {
                "username": "user1",
                "password": "TestPassword123!"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        # Перевіряємо вхід із неправильним паролем
        response = self.client.post(
            "/api/token/",
            {
                "username": "user1",
                "password": "wrong_password"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_refresh_token(self):
        # Перевіряємо оновлення access-токена
        refresh = RefreshToken.for_user(self.user1)

        response = self.client.post(
            "/api/token/refresh/",
            {"refresh": str(refresh)},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_verify_token(self):
        # Перевіряємо дійсний access-токен
        refresh = RefreshToken.for_user(self.user1)

        response = self.client.post(
            "/api/token/verify/",
            {"token": str(refresh.access_token)},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trainers_list(self):
        # Перевіряємо отримання списку тренерів
        response = self.client.get("/api/trainers/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trainers_cannot_be_created(self):
        # TrainerViewSet дозволяє лише читання
        self.authenticate(self.user1)

        response = self.client.post(
            "/api/trainers/",
            {
                "name": "New Trainer",
                "specialization": "Fitness",
                "experience_years": 3
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_classes_list(self):
        # Перевіряємо отримання списку занять
        response = self.client.get("/api/classes/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_classes_detail(self):
        # Перевіряємо отримання конкретного заняття
        response = self.client.get(
            f"/api/classes/{self.gym_class.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Morning Yoga")

    def test_create_class_authenticated(self):
        # Авторизований користувач створює заняття
        self.authenticate(self.user1)

        response = self.client.post(
            "/api/classes/",
            {
                "title": "Pilates",
                "trainer": self.trainer.id,
                "date": str(date.today() + timedelta(days=10)),
                "duration": 45,
                "max_participants": 12,
                "booked_places": 0
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Перевіряємо, що власник встановлений автоматично
        new_class = GymClass.objects.get(id=response.data["id"])
        self.assertEqual(new_class.owner, self.user1)

    def test_create_class_without_auth(self):
        # Неавторизований користувач не може створити заняття
        response = self.client.post(
            "/api/classes/",
            {"title": "Pilates"},
            format="json"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]
        )

    def test_update_own_class(self):
        # Власник може змінювати своє заняття
        self.authenticate(self.user1)

        response = self.client.patch(
            f"/api/classes/{self.gym_class.id}/",
            {"title": "Updated Yoga"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.gym_class.refresh_from_db()
        self.assertEqual(self.gym_class.title, "Updated Yoga")

    def test_update_other_users_class(self):
        # Інший користувач не може змінювати чуже заняття
        self.authenticate(self.user2)

        response = self.client.patch(
            f"/api/classes/{self.gym_class.id}/",
            {"title": "Changed by user2"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.gym_class.refresh_from_db()
        self.assertEqual(self.gym_class.title, "Morning Yoga")

    def test_delete_own_class(self):
        # Власник може видалити своє заняття
        self.authenticate(self.user1)

        response = self.client.delete(
            f"/api/classes/{self.gym_class.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            GymClass.objects.filter(id=self.gym_class.id).exists()
        )

    def test_delete_other_users_class(self):
        # Інший користувач не може видалити чуже заняття
        self.authenticate(self.user2)

        response = self.client.delete(
            f"/api/classes/{self.gym_class.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            GymClass.objects.filter(id=self.gym_class.id).exists()
        )

    def test_invalid_duration(self):
        # Тривалість заняття повинна бути більшою за нуль
        self.authenticate(self.user1)

        response = self.client.post(
            "/api/classes/",
            {
                "title": "Invalid Class",
                "trainer": self.trainer.id,
                "date": str(date.today() + timedelta(days=3)),
                "duration": 0,
                "max_participants": 10
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_booked_places_exceed_capacity(self):
        # Кількість зайнятих місць не може перевищувати максимальну
        self.authenticate(self.user1)

        response = self.client.post(
            "/api/classes/",
            {
                "title": "Overbooked Class",
                "trainer": self.trainer.id,
                "date": str(date.today() + timedelta(days=3)),
                "duration": 60,
                "max_participants": 5,
                "booked_places": 10
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_available_classes(self):
        # Перевіряємо список занять із вільними місцями
        response = self.client.get("/api/classes/available/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Наше заняття має 8 вільних місць
        self.assertEqual(response.data[0]["available_places"], 8)

    def test_create_booking_authenticated(self):
        # Авторизований користувач створює бронювання
        self.authenticate(self.user2)

        response = self.client.post(
            "/api/bookings/",
            {
                "gym_class": self.gym_class.id,
                "client_name": "Jane Doe",
                "client_email": "jane@example.com"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Перевіряємо власника нового бронювання
        booking = Booking.objects.get(id=response.data["id"])
        self.assertEqual(booking.owner, self.user2)

    def test_create_booking_without_auth(self):
        # Без авторизації бронювання створити не можна
        response = self.client.post(
            "/api/bookings/",
            {
                "gym_class": self.gym_class.id,
                "client_name": "Jane Doe",
                "client_email": "jane@example.com"
            },
            format="json"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]
        )

    def test_update_own_booking(self):
        # Власник може редагувати своє бронювання
        self.authenticate(self.user1)

        response = self.client.patch(
            f"/api/bookings/{self.booking.id}/",
            {"client_name": "Updated Name"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.client_name, "Updated Name")

    def test_update_other_users_booking(self):
        # Інший користувач не може редагувати чуже бронювання
        self.authenticate(self.user2)

        response = self.client.patch(
            f"/api/bookings/{self.booking.id}/",
            {"client_name": "Changed Name"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_own_booking(self):
        # Власник може видалити своє бронювання
        self.authenticate(self.user1)

        response = self.client.delete(
            f"/api/bookings/{self.booking.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_delete_other_users_booking(self):
        # Інший користувач не може видалити чуже бронювання
        self.authenticate(self.user2)

        response = self.client.delete(
            f"/api/bookings/{self.booking.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
