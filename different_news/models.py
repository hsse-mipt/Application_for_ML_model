from django.db import models


# Create your models here.
class News(models.Model):
    title = models.TextField(
        verbose_name='Заголовок',
        max_length=200
    )
    description = models.TextField(
        verbose_name='Новость'
    )
    link = models.URLField(
        verbose_name='Ссылка',
        max_length=2048,
        unique=True
    )
    published = models.DateTimeField(
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
