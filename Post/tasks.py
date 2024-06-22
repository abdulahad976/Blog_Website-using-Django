# tasks.py

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timezone.timedelta(minutes=1)
    inactive_users = User.objects.filter(last_login__lt=threshold, is_active=True)

    deactivated_users = []

    for user in inactive_users:
        try:
            user.is_active = False
            user.save()
            send_deactivation_email.delay(user.email)
            deactivated_users.append(user)
        except Exception as e:
            logger.error(f"Failed to deactivate user {user.username}: {str(e)}")

    logger.info(f"Deactivated Users: {deactivated_users}")

@shared_task
def send_deactivation_email(email):
    subject = 'Your account has been deactivated'
    message = 'Your account has been deactivated due to inactivity.'
    from_email = 'smallinfo.nature@gmail.com'
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Deactivation email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send deactivation email to {email}: {str(e)}")

@shared_task()
def inactive_users():
    inActiveUsers = User.objects.filter(is_active=False)
    for user in inActiveUsers:
        send_reactivation_email.delay(user.email)

@shared_task()
def send_reactivation_email(email):
    subject = 'You can still Reactivate you Account'
    message = 'Your account has been deactivated due to inactivity.'
    from_email = 'Account Reactivation'
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Reactivation email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send Reactivation email to {email}: {str(e)}")
