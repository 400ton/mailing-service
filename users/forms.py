from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from mailings.forms import StyleFormsMixin

from users.models import User


class RegisterForm(StyleFormsMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def label_from_instance(self, obj):
        # Переводим поля формы на русский язык
        if self.fields['password1']:
            self.fields['password1'].label = 'Пароль'
        if self.fields['password2']:
            self.fields['password2'].label = 'Подтверждение пароля'

        return super().label_from_instance(obj)


class UpdateForm(StyleFormsMixin, UserChangeForm):

    # password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'num_phone', 'avatar', 'country']

    # def clean_password1(self):
    #     # Получаем первый пароль
    #     password1 = self.cleaned_data.get("password1")
    #     # Получаем второй пароль
    #     password2 = self.cleaned_data.get("password2")
    #     # Проверяем, что оба пароля совпадают
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Пароли должны совпадать.")
    #     return password2
