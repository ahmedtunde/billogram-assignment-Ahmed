from datetime import timedelta
from decimal import Decimal as D

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from num2words import num2words
from billogram.discountservice.models import User, DiscountCode
from billogram.utils.helpers import (EmailSubjects, send_email)
from billogram.utils.send_emails import SendEmail

FRONTEND_URL = settings.FRONTEND_URL




@shared_task(name='expired_discount_codes')
def expired_discount_codes():
    current_date = timezone.now()
    discount_codes = DiscountCode.objects.filter(status="UNUSED",
                                valid_till=current_date)
    for codes in discount_codes:
        codes.save()
        user = user
        discount_code=codes.first()
        details = {
            'user_first_name': user.first_name,
            'discount_code': discount_code
        }
        send_email.delay(user_email=user.email, details=details)



@shared_task(name='send_email_async')
def send_email_async(*args, **kwargs):
    return send_email(*args, **kwargs)



@shared_task(name='send_custom_email')
def send_custom_email(template, subject, recipient_email, details):
    to_email = [recipient_email]
    context = {
        'domain': FRONTEND_URL,
    }
    context.update(details)
    send_mail = SendEmail(template, context, subject, to_email)
    return send_mail.send()



@shared_task(name='send_discount_code_usage_email')
def send_discount_code_usage_email(**kwargs):
    """ Send discount code email to Brands """
    template = 'email_alerts/DiscountCodeUsage.html'
    subject = "Discount Code Usage Email"
    user_email = kwargs.get('user_email')
    full_name = kwargs.get('full_name')
    discountcode = kwargs.get('discountcode')
    details = {
        'full_name': full_name,
        'discountcode': discountcode
    }
    send_custom_email(template, subject, user_email, details)
