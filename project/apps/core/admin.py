# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from core.models import *


class EmailAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('subject', 'body', 'sender', 'to', 'cc', 'reply_to')
    list_display = ('created_at', 'subject', 'to')
    list_filter = ('is_sent', 'created_at')


admin.site.register(Email, EmailAdmin)


class EmailEventAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('created_at', 'email', 'type')
    list_display = ('type', )
    list_filter = ('created_at', 'type')


admin.site.register(EmailEvent, EmailEventAdmin)


class CustomerAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name', 'email', 'id')
    list_display = ('name', 'email', 'id')


admin.site.register(Customer, CustomerAdmin)
