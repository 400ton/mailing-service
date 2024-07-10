from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import (HomeView, ClientsCreateView, ClientsUpdateView, ClientsListView, ClientsDeleteView,
                            MailingCreateView, MailingUpdateView, MailingDeleteView,
                            MessageCreateView, MailingListView, MessageUpdateView, MessageDeleteView,
                            MailingLogListView, MailingLogDetailView, MessageListView, MessageDetailView, toggle_active)

app_name = MailingsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('create-client/', ClientsCreateView.as_view(), name='create_client'),
    path('update-client/<int:pk>', ClientsUpdateView.as_view(), name='update_client'),
    path('list-client/', ClientsListView.as_view(), name='list_client'),
    path('delete-client/<int:pk>', ClientsDeleteView.as_view(), name='delete_client'),

    path('list-mailing/', MailingListView.as_view(), name='list_mailing'),
    path('creating-mailing/', MailingCreateView.as_view(), name='creating_mailing'),
    path('update-mailing/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete_mailing/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailing/toggle_active/<int:pk>', toggle_active, name='toggle_active'),


    path('list-message/', MessageListView.as_view(), name='list_message'),
    path('create-message/', MessageCreateView.as_view(), name='create_message'),
    path('detail-message/<int:pk>', MessageDetailView.as_view(), name='detail_message'),
    path('update-message/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('delete-message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('list-log/', MailingLogListView.as_view(), name='list_log'),
    path('log-detail/<int:pk>', MailingLogDetailView.as_view(), name='detail_log'),
]
