from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



# Modelo para el desarrollador
class Developer(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


# Modelo para el género/características
class Genre(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


# Modelo para la plataforma
class Plataform(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


# Modelo para la tienda
class Store(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


# Modelo para el videojuego
class Video_game(models.Model):
    name = models.TextField()
    url_inf = models.URLField()
    url_img = models.URLField()
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    discount = models.IntegerField(validators=[MinValueValidator(0)])
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    description = models.TextField()
    release_date = models.DateField(null=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    plataform = models.ForeignKey(Plataform, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

