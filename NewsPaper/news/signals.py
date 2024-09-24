from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import notify_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_category_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        notify_new_post.delay(instance.pk)
