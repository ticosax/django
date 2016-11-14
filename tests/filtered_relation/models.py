from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


@python_2_unicode_compatible
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author,
                               related_name='books',
                               related_query_name='book',
                               on_delete=models.CASCADE)
    editor = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
