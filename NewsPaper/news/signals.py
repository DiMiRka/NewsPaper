from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from NewsPaper import settings


def send_notifications(preview, pk, user, name, subscribers):
    html_content = render_to_string(
        'post_created_message.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}',
            'name': user
        }
    )

    msg = EmailMultiAlternatives(
        subject=name,
        body='',
        from_email=settings.EMAIL_ADMIN,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_category_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []
        name = None

        for c in categories:
            subscribers = c.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]
            for n in subscribers:
                name = n

        send_notifications(instance.preview(), instance.pk, name, instance.name, subscribers_emails)
