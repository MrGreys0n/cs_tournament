from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Player(models.Model):
    team = models.ForeignKey(
        'Team',
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Команда"
    )
    name = models.CharField(max_length=20, verbose_name="Имя")
    slug = models.SlugField(max_length=20, db_index=True, verbose_name="URL", unique=True, default=None)

    def get_absolute_url(self):
        return reverse('player', kwargs={'player_slug': self.slug})

    def __str__(self):
        return "{} ({})".format(self.name, self.team)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Team(models.Model):
    name = models.CharField(max_length=30, db_index=True, verbose_name="Название")
    is_full = models.BooleanField(verbose_name="Полная")
    rating = models.IntegerField(verbose_name="Рейтинг")
    contacts = models.CharField(max_length=30, verbose_name="Контакты")
    slug = models.SlugField(max_length=20, db_index=True, verbose_name="URL", unique=True, default=None)

    def get_absolute_url(self):
        return reverse('team', kwargs={'team_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
