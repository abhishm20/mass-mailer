# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from core.models import Customer


def run():
    customer_count = Customer.objects.all().count()
    to_be_created = 100000 - customer_count

    customers = [
        Customer(
            name=f"customer_{i}",
            email=f"customer_{i}@gmail.com",
        )
        for i in range(to_be_created)
    ]
    print("Created customers: ", len(Customer.objects.bulk_create(customers)))
