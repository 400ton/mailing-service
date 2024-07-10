from django.forms import ModelForm

from mailings.models import Message, Clients, Mailing


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


class ClientsForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Clients
        exclude = ('owner','is_active',)


class MailingForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ['owner', 'is_active',]
