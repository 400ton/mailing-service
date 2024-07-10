from django.forms import ModelForm

from blog.models import Blog


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'is_published':
                field.widget.attrs['class'] = 'switch'


class BlogForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'text', 'image')


class BlogUpdateForm(StyleFormsMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'text', 'image', 'is_published')
