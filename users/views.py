import secrets

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import RegisterForm, UpdateForm
from users.models import User


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'
    template_name = 'users/users_list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(is_superuser=False, is_staff=False)
        return queryset


@permission_required('users.view_user')
def block_user(self, pk):
    user = User.objects.get(pk=pk)
    user.is_active = {user.is_active: False,
                      not user.is_active: True}[True]
    user.save()
    return redirect(reverse('users:list_users'))


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Регистрация аккаунта'
        return context_data

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.set_password(user.password)
        verification_code = secrets.token_hex(16)
        user.verification_code = verification_code
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email.confirm/{verification_code}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        user.save()
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Профиль'
        return context_data


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        # Сохраняем новый пароль
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактировать профиль'
        return context_data

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, verification_code):
    user = get_object_or_404(User, verification_code=verification_code)
    if user:
        user.is_active = True
        user.verification_code = None
        user.save()
        return redirect(reverse("users:login"))


class GeneratePasswordView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                password = User.objects.make_random_password(length=8)
                user.set_password(password)
                user.save()
                send_mail(
                    'Смена пароля',
                    f'Здравствуйте.Вы запросили генерацию нового пароля для локального сайта. '
                    f'Ваш новый пароль: {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return redirect(reverse("users:login"))
            except User.DoesNotExist:
                messages.error(self.request, "Такого пользователя не существует.")
                return redirect(reverse("users:reset_password"))
        else:
            messages.error(self.request, "Произошла ошибка при генерации пароля.")
            return super().form_invalid(form)
