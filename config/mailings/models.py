from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Clients(models.Model):
    email = models.EmailField(unique=True, max_length=35, verbose_name='Почта')
    family_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество', **NULLABLE)
    comment = models.TextField(verbose_name='Коммент', **NULLABLE)

    def __str__(self):
        return f'{self.email} '

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.message}'


class Mailing(models.Model):
    list_period = (
        ('once_day', 'раз в день'),
        ('once_week', 'раз в неделю'),
        ('once_month', 'раз в месяц')
    )

    list_status = (
        ('created', 'создана'),
        ('executing', 'запущена'),
        ('finished', 'закончена успешно'),
        ('error', 'законечена с ошибками')
    )

    start_mailing = models.DateTimeField(default=timezone.now, verbose_name='Начало рассылки')
    next_mailing = models.DateTimeField(default=timezone.now, verbose_name='Следующая рассылка')
    end_mailing = models.DateTimeField(default=timezone.now, verbose_name='Конец рассылки', **NULLABLE)
    periodicity = models.CharField(max_length=100, choices=list_period, verbose_name='Периодичность')
    status = models.CharField(max_length=100, choices=list_status, verbose_name='Статус')

    clients = models.ForeignKey(Clients, on_delete=models.SET_NULL, verbose_name='Клиенты', **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='Сообщение', **NULLABLE )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.owner} {self.start_mailing} {self.periodicity} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log_mailing(models.Model):
    ...
