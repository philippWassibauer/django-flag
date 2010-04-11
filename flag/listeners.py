from django.conf import settings
from django.core.mail import mail_managers
from django.db.models import get_model
from django.db.models.signals import post_save

EMAIL_NOTIFY_CREATOR = getattr('settings', 'FLAG_EMAIL_NOTIFY_CREATOR', False)
EMAIL_NOTIFY_MANAGERS = getattr('settings', 'FLAG_EMAIL_NOTIFY_MANAGERS', False)


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
Content: "%s"
Accusation: "%s"
""" % (accused, flagged_object, accusation)

        accused.email_user(subject, message)


def _post_create_email_notify_managers(sender, instance, created, **kwargs):
    """
    Sends a new flag notification email to the managers.
    """
    if created:
        accused = instance.flagged_content.creator
        accusation = instance.comment
        informant = instance.flagged_content.creator
        flagged_object = unicode(instance.flagged_content.content_object)
        flagged_object_url = None
        if hasattr(flagged_object, 'get_absolute_url'):
            flagged_object_url = flagged_object.get_absolute_url()
        subject = """"%s" got flagged as inappropriate""" % flagged_object
        message = \
"""
Content: "%s"
Content URL: "%s"
Informant: "%s"
Accused: "%s"
Accusation: "%s"
""" % (flagged_object, flagged_object_url, informant, accused, accusation)

        mail_managers(subject, message)


def start_listening():
    flag_instance_model = get_model('flag', 'FlagInstance')

    if EMAIL_NOTIFY_CREATOR and not settings.DEBUG:
        post_save.connect(_post_create_email_notify_creator, sender=flag_instance_model)

    if EMAIL_NOTIFY_MANAGERS and not settings.DEBUG:
        post_save.connect(_post_create_email_notify_managers, sender=flag_instance_model)
