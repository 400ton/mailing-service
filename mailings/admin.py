from django.contrib import admin

from mailings.models import Clients, Message, Mailing, MailingLog


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('email', 'family_name', 'first_name', 'middle_name')
    list_filter = ('email',)
    search_fields = ('email', 'family_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    list_filter = ('title', 'owner')
    search_fields = ('title', 'owner')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_mailing', 'periodicity', 'status')
    list_filter = ('owner', 'start_mailing', 'periodicity', 'clients', 'status')
    search_fields = ('owner', 'start_mailing', 'periodicity', 'clients', 'status')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'status', 'server_response')
    list_filter = ('last_attempt', 'status', 'server_response')
    search_fields = ('last_attempt', 'status', 'server_response')
