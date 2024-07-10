# Generated by Django 4.2 on 2024-07-03 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailinglog',
            options={'ordering': ('-last_attempt',), 'permissions': [('change_is_active', 'Может отключать рассылки.')], 'verbose_name': 'Лог рассылки', 'verbose_name_plural': 'Логи рассылок'},
        ),
        migrations.RenameField(
            model_name='mailinglog',
            old_name='date_of_last_attempt',
            new_name='last_attempt',
        ),
        migrations.RemoveField(
            model_name='mailinglog',
            name='status_of_last_attempt',
        ),
        migrations.AddField(
            model_name='mailing',
            name='clients',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailings.clients', verbose_name='Клиенты'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mailings.message', verbose_name='сообщение'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailing',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='mailinglog',
            name='status',
            field=models.CharField(choices=[('successfully', 'успешно'), ('not_successful', 'не успешно')], default=None, verbose_name='статус попытки'),
        ),
        migrations.AddField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'создана'), ('executing', 'запущена'), ('finished', 'закончена успешно'), ('error', 'закончена с ошибками')], max_length=100, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='mailinglog',
            name='server_response',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ответ почтового сервера'),
        ),
    ]