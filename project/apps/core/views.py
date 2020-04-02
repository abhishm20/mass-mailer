# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from core import utility
from core.constant import *
from core.models import Email, Customer, EmailEvent
from core.serializers import EmailEventSerializer, CustomerSerializer, EmailSerializer


@api_view(['GET'])
def mark_read_email(request):
    if request.GET.get('eid'):
        email = Email.objects.get(tracking_id=request.GET.get('eid'))
        d = {
            'created_at': utility.get_current_time(),
            'email': email.id,
            'type': EMAIL_OPEN_EVENT[0]
        }
        ser = EmailEventSerializer(data=d)
        ser.is_valid(raise_exception=True)
        ser.save()
        return HttpResponse({'message': 'Thank you for using Finshots.'}, status=200)
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


@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST' and request.POST.get('send_to_all'):
        from core.tasks import send_email_to_all_task
        send_email_to_all_task.delay()
    email_page = request.GET.get('email_page', 1)
    customer_page = request.GET.get('customer_page', 1)

    # Get Customer data
    customers = Customer.objects.all()

    # Get Email data
    emails = Email.objects.prefetch_related(
        Prefetch('events', to_attr='clicked_events', queryset=EmailEvent.objects.filter(type=EMAIL_CLICK_EVENT[0])),
        Prefetch('events', to_attr='opened_events', queryset=EmailEvent.objects.filter(type=EMAIL_OPEN_EVENT[0]))
    )
    emails_res = []
    for e in emails:
        emails_res.append({
            'clicked_count': len(e.clicked_events),
            'email_data': e,
            'opened_count': len(e.opened_events)
        })

    # Customer pagination
    customer_paginator = Paginator(customers, 10)
    try:
        customers = customer_paginator.page(customer_page)
    except PageNotAnInteger:
        customers = customer_paginator.page(1)
    except EmptyPage:
        customers = customer_paginator.page(customer_paginator.num_pages)

    # Email pagination
    email_paginator = Paginator(emails_res, 10)
    try:
        emails = email_paginator.page(email_page)
    except PageNotAnInteger:
        emails = email_paginator.page(1)
    except EmptyPage:
        emails = email_paginator.page(customer_paginator.num_pages)
    return render(request, 'index.html', {'customers': customers, 'emails': emails, 'title': "Mass Mailer"})
