from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rating = 0
        comments_rating = 0
        posts_comments_rating = 0
        for p in Post.objects.filter(author=self):
            posts_rating += p.rating
        for c in Comment.objects.filter(user=self.user):
            comments_rating += c.rating
        for pc in Comment.objects.filter(post__author=self):
            posts_comments_rating += pc.rating

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новости')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_in = models.DateField(auto_now_add=True)
    article_or_news = models.CharField(max_length=2, choices=POSITIONS, default=news)
    category = models.ManyToManyField(Category, through='PostCategory')
    name = models.CharField(max_length=140, default=article_or_news)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'{self.name.title()}: {self.rating}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
