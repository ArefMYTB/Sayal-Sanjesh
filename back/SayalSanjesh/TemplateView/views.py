from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse
from ..models import Bills, WaterMetersConsumptions
from django.db.models import Sum
from django.core.exceptions import BadRequest
from persiantools import characters, digits


def bill(request, bill_id, random_token):
    template = loader.get_template('index.html')
    bill_object = Bills.objects.get(bill_id=bill_id)
    if bill_object.bill_link_validation is False:
        return HttpResponse(status=410)

    period_days = bill_object.bill_end_date - bill_object.bill_start_date
    try:
        consumptions = WaterMetersConsumptions.objects.filter(create_time__gte=bill_object.bill_start_date,
                                                              create_time__lte=bill_object.bill_end_date)
        period_consumption = consumptions.aggregate(Sum('value'))
        period_sum = float('{:.2f}'.format(period_consumption['value__sum']))
        avg_consumption = period_sum / period_days.days
    except:
        avg_consumption = None
        period_sum = None
    context = {
        "userInfo": {
            'first_name': bill_object.bill_user.user_name,
            'last_name': bill_object.bill_user.user_lastname,
            'address': '',
            'phone_number': bill_object.bill_user.user_phone
        },
        'billInfo': {
            'create_date': {
                # digits.en_to_fa("0987654321")
                'year': bill_object.bill_create_date.year,
                'month': bill_object.bill_create_date.month,
                'day': bill_object.bill_create_date.day
            },
            'from_date': {
                'year': bill_object.bill_start_date.year,
                'month': bill_object.bill_start_date.month,
                'day': bill_object.bill_start_date.day
            },
            'to_date': {
                'year': bill_object.bill_end_date.year,
                'month': bill_object.bill_end_date.month,
                'day': bill_object.bill_end_date.day
            },
            # to - from >> time

            'period_days': period_days.days,
            # sum of consumptions in periods day
            'period_consumption': period_sum,
            # period_cons % count day(period days)
            'avg_consumption': avg_consumption,
            'id': bill_object.bill_id,
            'deadline': {
                'year': bill_object.payment_dead_line.year,
                'month': bill_object.payment_dead_line.month,
                'day': bill_object.payment_dead_line.day
            },
            # price in bill table
            'payable_amount': int(bill_object.bill_price),
            'counter_serial': bill_object.bill_water_meter.water_meter_serial,
            'code': bill_object.bill_serial,
            # search for change number to str
            'payable_amount_letters': digits.to_word(int(bill_object.bill_price))
        }
    }
    # Bills.objects.update(bill_link_validation=False)
    return HttpResponse(template.render(context, request))
