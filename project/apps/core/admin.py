# -*- coding: utf-8 -*-


from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from core.models import *
from core.serializers import EmailSerializer
from core.tasks import send_email_task


class EmailAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('subject', 'body', 'sender', 'to', 'cc', 'reply_to')
    list_display = ('created_at', 'subject', 'to')
    list_filter = ('is_sent', 'is_seen', 'created_at')
    actions = ['resend_emails']

    def resend_emails(self, request, queryset):
        count = queryset.count()
        for i in queryset:
            email_data = EmailSerializer(i).data
            send_email_task.delay(email_data)
        self.message_user(request, "%s email successfully resent." % count)


admin.site.register(Email, EmailAdmin)
