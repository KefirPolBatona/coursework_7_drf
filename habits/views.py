from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import CustomPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """
        Привязывает пользователя к создаваемой им привычке.
        """

        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает публичные привычки.
        """

        return super().get_queryset().filter(is_publicity=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_object(self):
        """
        Возвращает публичную или пользовательскую привычку.
        """

        habit = super().get_object()
        user = self.request.user
        if habit.user == user or habit.is_publicity:
            return habit
        else:
            raise PermissionDenied("Ограничено правами доступа")


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]


class HabitOwnerListAPIView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        """
        Возвращает привычки текущего пользователя.
        """

        user = self.request.user
        return super().get_queryset().filter(user=user)
