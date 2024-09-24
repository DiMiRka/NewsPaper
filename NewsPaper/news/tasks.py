import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from .models import Category, PostCategory, Post


@shared_task
def notify_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    for c in categories:
        subscribers = c.subscribers.all()
        for s in subscribers:
            subscriber_email = s.email
            subscriber_name = s
            send_notifications(post.preview(), post.pk, subscriber_name, post.name, subscriber_email)


def send_notifications(preview, pk, user, name, subscriber):
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
        to=[subscriber]
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send(posts_send, user, mail):
    html_content = render_to_string(
        'send_every_week.html',
        {
            'posts': posts_send,
            'name': user,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новые посты за неделю в твоём любимом разделе!',
        body='',
        from_email=settings.EMAIL_ADMIN,
        to=[mail]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_mails():
    categories = Category.objects.all()
    for c in categories:
        post_info = {}
        subscribers = c.subscribers.all()
        today = datetime.datetime.now()
        last_week = today - datetime.timedelta(days=7)
        posts = PostCategory.objects.filter(category=c, post__time_in__gte=last_week)
        for p in posts:
            post_info[p.post.pk] = p.post.name
        for s in subscribers:
            name = s
            mail = s.email
            send(posts_send=post_info, user=name, mail=mail)
