from rest_framework import serializers

from habits.models import Habit
from habits.validators import UsefulHabitValidator, PleasantHabitValidator, LeadTime


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            UsefulHabitValidator(associated_habit='associated_habit',
                                 reward='reward',
                                 is_pleasant_habit='is_pleasant_habit'),
            PleasantHabitValidator(is_pleasant_habit='is_pleasant_habit',
                                   associated_habit='associated_habit',
                                   reward='reward'),
            LeadTime(time_to_complete='time_to_complete'),
        ]
