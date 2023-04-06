from django.template.defaultfilters import slugify
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

from django.urls import reverse
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
User = get_user_model()


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.author.id, filename)


class Article(models.Model):

    title = models.CharField(max_length=255)

    body = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    tags = TaggableManager()
    banner_image = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)


class Comment(models.Model):  # new

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):

        return self.comment

    def get_absolute_url(self):

        return reverse('article_list')


class LikeArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    articles= models.ManyToManyField(Article)