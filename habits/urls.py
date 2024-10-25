from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView, \
    HabitListAPIView, HabitOwnerListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='create'),
    path('list/', HabitListAPIView.as_view(), name="list"),
    path('detail/<int:pk>/', HabitRetrieveAPIView.as_view(), name='detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='delete'),

    path('user/', HabitOwnerListAPIView.as_view(), name="list-owner"),
]
