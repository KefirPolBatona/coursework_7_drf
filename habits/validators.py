from rest_framework.exceptions import ValidationError


class UsefulHabitValidator:
    """
    Валидация полезной привычки.
    """

    def __init__(self, associated_habit, reward, is_pleasant_habit):
        self.associated_habit = associated_habit
        self.reward = reward
        self.is_pleasant_habit = is_pleasant_habit

    def __call__(self, value):
        associated_habit = dict(value).get(self.associated_habit)
        reward = dict(value).get(self.reward)
        is_pleasant_habit = dict(value).get(self.is_pleasant_habit)

        if not is_pleasant_habit:
            if associated_habit and reward:
                raise ValidationError('Необходимо указать или вознаграждение, или приятную привычку')
            if not associated_habit and not reward:
                raise ValidationError('Необходимо указать или вознаграждение, или приятную привычку')
            if associated_habit:
                if not associated_habit.is_pleasant_habit:
                    raise ValidationError('Необходимо указать приятную привычку')


class PleasantHabitValidator:
    """
    Валидация приятной привычки.
    """

    def __init__(self, is_pleasant_habit, associated_habit, reward):
        self.is_pleasant_habit = is_pleasant_habit
        self.associated_habit = associated_habit
        self.reward = reward

    def __call__(self, value):
        is_pleasant_habit = dict(value).get(self.is_pleasant_habit)
        associated_habit = dict(value).get(self.associated_habit)
        reward = dict(value).get(self.reward)

        if is_pleasant_habit:
            if associated_habit or reward:
                raise ValidationError('У приятной привычки не должно быть вознаграждения и связанной привычки')


class LeadTime:
    """
    Валидация времени выполнения привычки.
    """

    def __init__(self, time_to_complete):
        self.time_to_complete = time_to_complete

    def __call__(self, value):
        time_to_complete = dict(value).get(self.time_to_complete)

        if time_to_complete:
            if time_to_complete < 1 or time_to_complete > 120:
                raise ValidationError('Время на выполнение может быть от 1 до 120 минут')
