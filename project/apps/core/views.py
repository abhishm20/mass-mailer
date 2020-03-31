# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from PIL import Image
from django.http import HttpResponse
from rest_framework.decorators import api_view

from core import utility
from core.constant import *
from core.models import Email
from core.serializers import EmailEventSerializer


@api_view(['GET'])
def mark_read_email(request):
    if request.GET.get('eid'):
        Email.objects.select_for_update().filter(tracking_id=request.GET['eid']).update(is_seen=True)
    red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    res = HttpResponse(content_type="image/png")
    red.save(res, "JPEG")
    return res


@api_view(['GET'])
def mark_email_clicked(request):
    if request.GET.get('eid'):
        email = Email.objects.get(tracking_id=request.GET.get('eid'))
        d = {
            'created_at': utility.get_current_time(),
            'email': email.id,
            'type': EMAIL_CLICK_EVENT[0]
        }
        ser = EmailEventSerializer(data=d)
        ser.is_valid(raise_exception=True)
        ser.save()
        return HttpResponse({'message': 'Thank you for using Finshots.'}, status=200)
    else:
        return HttpResponse({'error': 'There is some problem with the link.'}, status=400)
