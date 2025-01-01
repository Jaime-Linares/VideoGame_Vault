from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



# modelo para el desarrollador
class Developer(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


# modelo para el género/características
class Genre(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


# modelo para la plataforma
class Plataform(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


# modelo para la tienda
class Store(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


# modelo para el videojuego
class Video_game(models.Model):
    name = models.TextField(blank=False, null=False)
    url_inf = models.URLField(null=False)
    url_img = models.URLField(null=False)
    price = models.FloatField(validators=[MinValueValidator(0.0)], null=False)
    discount = models.IntegerField(validators=[MinValueValidator(0)], null=False)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], null=False)
    description = models.TextField(blank=True, null=False)
    release_date = models.DateField(null=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    plataform = models.ForeignKey(Plataform, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

