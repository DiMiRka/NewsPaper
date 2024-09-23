from django import template

register = template.Library()

Censor_list = ['херня', 'гомосек']


@register.filter()
def censor(text):
    for word in Censor_list:
        text = text.replace(word[1:], '*' * len(word[1:]))
    return text


@register.filter()
def publication_type(value):
    if value == 'NE':
        text = 'Новость'
    else:
        text = 'Статья'
    return text

