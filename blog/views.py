from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.forms import BlogForm, BlogUpdateForm
from blog.models import Blog


class BlogList(ListView):
    model = Blog

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список статей'
        return context_data


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list_blog')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание статьи'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogUpdateForm
    success_url = reverse_lazy('blog:list_blog')
    permission_required = 'update_blog'

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактировать статью'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogDetail(DetailView):
    model = Blog
    fields = ('title', 'text', 'image', )
    success_url = reverse_lazy('blog:list_blog')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'О статье'
        return context_data

    def get_object(self, queryset=None):
        """Счетчик просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list_blog')
    permission_required = 'delete_blog'

    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удалить статью'
        return context_data
