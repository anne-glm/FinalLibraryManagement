from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Borrowing  

@shared_task
def send_due_date_reminder():
    today = timezone.now().date()
    borrowings = Borrowing.objects.filter(due_date=today, return_date__isnull=True)

    for borrowing in borrowings:
        send_mail(
            'Book Due Date Reminder',
            f'Hi {borrowing.user.username},\n\nThe book "{borrowing.book.title}" is due today. Please return it as soon as possible.',
            'annegholami0@gmai.com', 
            [borrowing.user.email],
            fail_silently=False,
        )
