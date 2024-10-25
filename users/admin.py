from django.contrib import admin

from users.models import User

""" Отображает раздел "Пользователи" в админке """
admin.site.register(User)

