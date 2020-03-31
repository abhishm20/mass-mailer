# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from core.models import Email, EmailEvent


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class EmailEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailEvent
        fields = "__all__"
