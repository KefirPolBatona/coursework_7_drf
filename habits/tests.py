from datetime import timedelta, datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """
    Тестирование CRUD привычек.
    """

    def setUp(self):
        self.user = User.objects.create(email='test@gmail.com')
        self.owner = User.objects.create(email='test_1@gmail.com')

        self.pleasant_habit = Habit.objects.create(
            action="Действие 1",
            place="Место выполнения привычки 1",
            time=datetime.strptime('09:00', '%H:%M').time(),
            is_pleasant_habit=True,
            periodicity="1 time in 1 days",
            time_to_complete=60,
            user=self.owner,
        )
        self.useful_habit = Habit.objects.create(
            action="Действие 2",
            place="Место выполнения привычки 2",
            time=datetime.strptime('09:00', '%H:%M').time(),
            periodicity="1 time in 1 days",
            time_to_complete=60,
            is_publicity=True,
            user=self.owner,
            associated_habit=self.pleasant_habit,
        )
        self.useful_habit_with_reward = Habit.objects.create(
            action="Действие 3",
            place="Место выполнения привычки 3",
            time=datetime.strptime('10:00', '%H:%M').time(),
            periodicity="1 time in 1 days",
            time_to_complete=60,
            reward="reward test 3",
            is_publicity=True,
            user=self.owner,
        )
        self.useful_habit_non_publicity = Habit.objects.create(
            action="Действие 4",
            place="Место выполнения привычки 4",
            time=datetime.strptime('10:00', '%H:%M').time(),
            periodicity="1 time in 1 days",
            time_to_complete=60,
            is_publicity=False,
            user=self.owner,
            associated_habit=self.pleasant_habit,
        )
        self.useful_habit_user = Habit.objects.create(
            action="Действие 5",
            place="Место выполнения привычки 5",
            time=datetime.strptime('11:00', '%H:%M').time(),
            periodicity="1 time in 1 days",
            time_to_complete=30,
            is_publicity=False,
            user=self.user,
            associated_habit=self.pleasant_habit,
        )
        self.client.force_authenticate(user=self.owner)

    def test_habit_create_pleasant(self):
        """
        Создания приятной привычки.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 2",
            "place": "Место выполнения привычки 2",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
            "is_pleasant_habit": "True"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_habit_create_associated(self):
        """
        Создания привычки со связанной.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 3",
            "place": "Место выполнения привычки 3",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
            "is_publicity": True,
            "associated_habit": self.pleasant_habit.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_habit_create_reward(self):
        """
        Создание привычки с вознаграждением.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 3",
            "place": "Место выполнения привычки 3",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
            "reward": "Вознаграждение",
            "is_publicity": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_habit_create_reward_pleasant(self):
        """
        Создание приятной привычки с вознаграждением.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 4",
            "place": "Место выполнения привычки 4",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
            "reward": "Вознаграждение 4",
            "is_pleasant_habit": "True",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_not_valid_habit(self):
        """
        Создание привычки с вознаграждением и связанной привычкой.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 4",
            "place": "Место выполнения привычки 4",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
            "reward": "Вознаграждение 4",
            "is_pleasant_habit": "True",
            "associated_habit": self.pleasant_habit,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_habit_create_not_reward_not_pleasant(self):
        """
        Создание привычки без вознаграждения и без связанной привычки.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 1",
            "place": "Место выполнения привычки 1",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_habit_create_more_time(self):
        """
        Создание привычки с большим временем.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 2",
            "place": "Место выполнения привычки 2",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 160,
            "is_pleasant_habit": "True"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_habit_create_negative_time(self):
        """
        Создание привычки с отрицательным значением времени.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 2",
            "place": "Место выполнения привычки 2",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": -33,
            "is_pleasant_habit": "True"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_habit_create_pleasant_associated(self):
        """
        Создание приятной привычки со связанной.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 4",
            "place": "Место выполнения привычки 4",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
            "is_pleasant_habit": "True",
            "associated_habit": self.pleasant_habit,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_habit_create_associated_not_pleasant(self):
        """
        Создание привычки со связанной, связанная привычка без признака приятной.
        """

        url = reverse("habits:create")
        data = {
            "action": "Действие 4",
            "place": "Место выполнения привычки 4",
            "time": timedelta(minutes=12),
            "periodicity": "1 time in 1 days",
            "time_to_complete": 60,
            "is_pleasant_habit": "True",
            "associated_habit": self.useful_habit,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_habit_retrieve(self):
        """
        Вывод инфо о привычке, пользователь - владелец.
        """

        url = reverse("habits:detail", args=(self.useful_habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('place'),
            self.useful_habit.place
        )

    def test_habit_public_retrieve(self):
        """
        Вывод инфо о публичной привычке, пользователь - не владелец.
        """

        self.client.force_authenticate(user=self.user)
        url = reverse("habits:detail", args=(self.useful_habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('place'),
            self.useful_habit.place
        )

    def test_habit_not_publicity_retrieve(self):
        """
        Вывод инфо о непубличной привычки, пользователь - не владелец.
        """

        self.client.force_authenticate(user=self.user)
        url = reverse("habits:detail", args=(self.useful_habit_non_publicity.pk,))
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_update(self):
        """
        Редактирование привычки, пользователь - владелец.
        """

        url = reverse("habits:update", args=(self.pleasant_habit.pk,))
        data = {
            "time": timedelta(minutes=13),
            "is_pleasant_habit": True
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('time'),
            '00:13:00'
        )

    def test_habit_update_not_owner(self):
        """
        Редактирование привычки, пользователь - не владелец.
        """

        self.client.force_authenticate(user=self.user)
        url = reverse("habits:update", args=(self.pleasant_habit.pk,))
        data = {
            "time": timedelta(minutes=13),
            "is_pleasant_habit": True
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_update_unauthorized(self):
        """
        Редактирование привычки, пользователь - не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("habits:update", args=(self.pleasant_habit.pk,))
        data = {
            "time": timedelta(minutes=13),
            "is_pleasant_habit": True
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_habit_destroy(self):
        """
        Удаление привычки, пользователь - владелец.
        """

        url = reverse("habits:delete", args=(self.pleasant_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Habit.objects.all().count(), 4)

    def test_habit_destroy_not_owner(self):
        """
        Удаление привычки, пользователь - не владелец.
        """

        self.client.force_authenticate(user=self.user)
        url = reverse("habits:delete", args=(self.pleasant_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_destroy_unauthorized(self):
        """
        Удаление привычки, пользователь - не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("habits:delete", args=(self.pleasant_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_habit_list_owner(self):
        """
        Список привычек, пользователь - владелец привычек.
        """

        url = reverse('habits:list-owner')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_list_unauthorized(self):
        """
        Список привычек, пользователь - не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse('habits:list-owner')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_habit_list_publicity(self):
        """
        Список публичных привычек.
        """

        url = reverse('habits:list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['count'], 2)
        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)
