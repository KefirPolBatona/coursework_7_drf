from datetime import timedelta

import requests

from config import settings


def send_telegram_message(chat_id, message):
    """
    Отправка уведомления в Телеграм
    """

    params = {
        'text': message,
        'chat_id': chat_id,
    }
    requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage', params=params)


def get_next_reminder(current_date_reminder, periodicity):
    """
    Определение даты следующего напоминания.
    """

    if periodicity == '1 time in 1 days':
        return current_date_reminder + timedelta(minutes=1)
    elif periodicity == '1 time in 7 days':
        return current_date_reminder + timedelta(minutes=7)
