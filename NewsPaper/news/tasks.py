import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from .models import Category, PostCategory


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
