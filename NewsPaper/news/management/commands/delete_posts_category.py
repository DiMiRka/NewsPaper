from django.core.management.base import BaseCommand

from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удалить все публикации данной категории'
    missing_args_message = 'Вы не указали категорию'

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str, choices=[a['name'] for a in ([x for x in Category.objects.all().values('name')])])

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you really want to delete posts? yes/no')
        answer = input()
        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            Post.objects.filter(category__name=options['category'][0]).delete()
            self.stdout.write(self.style.SUCCESS("Posts deleted!"))
            return

        self.stdout.write(self.style.ERROR('Access denied'))

