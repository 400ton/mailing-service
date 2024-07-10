from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogList, BlogCreate, BlogUpdate, BlogDetail, BlogDelete

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogList.as_view(), name='list_blog'),
    path('create/', BlogCreate.as_view(), name='create_blog'),
    path('update/<int:pk>', BlogUpdate.as_view(), name='update_blog'),
    path('detail/<int:pk>', BlogDetail.as_view(), name='detail_blog'),
    path('delete/<int:pk>', BlogDelete.as_view(), name='delete_blog'),
]
