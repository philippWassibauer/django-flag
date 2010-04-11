from django.conf import settings
from django.core.mail import send_mail
from django.db.models import get_model
from django.db.models.signals import post_save

EMAIL_NOTIFY_CREATOR = getattr('settings', 'FLAG_EMAIL_NOTIFY_CREATOR', True) 


def _post_create_email_notify_creator(sender, instance, created, **kwargs):
    """
    Sends a new flag notification email to the creator of a flagged item.
    """
    if created:
        accused = instance.flagged_content.creator
        accusation = instance.comment
        flagged_object = unicode(instance.flagged_content.content_object)

        subject = """"%s" got flagged as inappropriate""" % flagged_object
        message = \
"""
Dear %s,

we received an accusation concerning your content. If you share the accusation,
please change or delete your content so that everyone is happy again. Our staff
also got informed and will check if you stuck to our terms of use.

Content: "%s"
Accusation: "%s"

""" % (accused, flagged_object, accusation)

        accused.email_user(subject, message)


def start_listening():
    flag_instance_model = get_model('flag', 'FlagInstance')

    if EMAIL_NOTIFY_CREATOR and not settings.DEBUG:
        post_save.connect(_post_create_email_notify_creator, sender=flag_instance_model)
