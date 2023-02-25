from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    title_en = models.CharField(
        blank=True, max_length=200, verbose_name='Имя (англ.)')
    title_jp = models.CharField(
        blank=True, max_length=200, verbose_name='Имя (яп.)')
    image = models.ImageField(
        null=True, upload_to='media', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey("self", on_delete=models.SET_NULL, null=True,
                                           blank=True, related_name='next_evolutions', verbose_name='Из кого эволюционировал')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='entities')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Время исчезновения')
    level = models.IntegerField(
        null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(
        null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(
        null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(
        null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(
        null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return self.pokemon.title
