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
    is_active = models.BooleanField(default=True, verbose_name='активность')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

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

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    list_period = (
        ('once_day', 'раз в день'),
        ('once_week', 'раз в неделю'),
        ('once_month', 'раз в месяц')
    )

    list_status = [
        ('created', 'создана'),
        ('executing', 'запущена'),
        ('finished', 'закончена успешно'),
        ('error', 'закончена с ошибками')]

    start_mailing = models.DateTimeField(default=timezone.now, verbose_name='Начало рассылки')
    next_mailing = models.DateTimeField(default=timezone.now, verbose_name='Следующая рассылка')
    end_mailing = models.DateTimeField(default=timezone.now, verbose_name='Конец рассылки', **NULLABLE)
    periodicity = models.CharField(max_length=100, choices=[('once_day', 'раз в день'), ('once_week', 'раз в неделю'),
                                                            ('once_month', 'раз в месяц')],
                                   verbose_name='Периодичность')
    status = models.CharField(max_length=100, choices=list_status, verbose_name='Статус', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активна')
    clients = models.ManyToManyField(Clients, verbose_name='Клиенты')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    @property
    def recipients(self):
        """
        Возвращает список email адресов клиентов для рассылки
        """
        return [client.email for client in self.clients.all()]

    def __str__(self):
        return f'{self.owner} {self.start_mailing} {self.periodicity} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    list_status = (
        ('successfully', 'успешно'),
        ('not_successful', 'не успешно'),
    )

    last_attempt = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    status = models.CharField(choices=list_status, default=None, verbose_name='статус попытки')
    server_response = models.CharField(max_length=50, verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='расписание', **NULLABLE)

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
        ordering = ('-last_attempt',)
        permissions = [
            ('change_is_active', 'Может отключать рассылки.'), ]

    def __str__(self):
        return f'{self.last_attempt} - {self.status} - {self.server_response}'
