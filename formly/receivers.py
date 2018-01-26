from django.db.models import signals
from django.dispatch import receiver

from formly.models import Survey


@receiver(signals.post_save, sender=Survey)
def handle_survey_save(sender, instance, created, **kwargs):
    if created:
        instance.pages.create()
