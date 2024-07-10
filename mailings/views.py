from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView

from mailings.forms import MessageForm, ClientsForm, MailingForm
from mailings.models import Mailing, Message, Clients, MailingLog
from users.models import User


@login_required
def toggle_active(request, pk):
    """
    Функция переключения статуса
    """
    mailing = Mailing.objects.get(pk=pk)
    # Переключаем статус is_active, если только рассылка не завершена
    if mailing.status != 'finished':
        mailing.is_active = {mailing.is_active: False,
                             not mailing.is_active: True}[True]
        mailing.save()
    else:
        messages.error(request, 'Рассылка завершена')
    return redirect(reverse('mailing:list_mailing'))


class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        context_data['count_mailing'] = len(Mailing.objects.all())
        count_active_mailings = Mailing.objects.filter(is_active=True).count()
        context_data['count_active_mailings'] = count_active_mailings
        unique_clients_count = Clients.objects.filter(is_active=True).distinct().count()
        context_data['count_unique_clients'] = unique_clients_count
        # all_posts = list(Blog.objects.filter(is_published=True))
        # context_data['random_blog_posts'] = sample(all_posts, min(3, len(all_posts)))
        return context_data


# Контроллеры для клиента
class ClientsCreateView(LoginRequiredMixin, CreateView):
    model = Clients
    form_class = ClientsForm
    success_url = reverse_lazy('mailing:list_client')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление клиента'
        return context_data

    def form_valid(self, form):
        new_client = form.save()
        new_client.owner = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientsListView(ListView):
    model = Clients

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Клиенты'
        return context_data


class ClientsUpdateView(LoginRequiredMixin, UpdateView):
    model = Clients
    form_class = ClientsForm
    success_url = reverse_lazy('mailing:list_client')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование клиента'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientsDeleteView(LoginRequiredMixin, DeleteView):
    model = Clients
    success_url = reverse_lazy('mailing:list_client')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление пользователя'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


# Контроллеры для рассылок
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Рассылки'
        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создать рассылку'
        return context_data

    def get_success_url(self):
        return reverse('mailing:list_mailing')

    def form_valid(self, form):
        new_mailing = form.save()
        new_mailing.owner = self.request.user
        new_mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list_mailing')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Обновить рассылку'
        return context_data


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list_mailing')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"


# Контроллеры для сообщений
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:list_message')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание сообщения'
        return context_data


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Сообщения'
        return context_data


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:list_message')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование "{self.object.title}"'
        return context_data


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:list_message')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление сообщения'
        return context_data


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Детали сообщения'
        return context_data


# Контроллеры для логов рассылок
class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Логи'
        return context_data


class MailingLogDetailView(LoginRequiredMixin, DetailView):
    model = MailingLog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object
