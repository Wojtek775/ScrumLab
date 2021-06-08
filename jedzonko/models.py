from django.db import models
from django.utils.text import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    ingredients = models.CharField(max_length=512)
    description = models.TextField()
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)
    directions = models.TextField()

    def __str__(self):
        return self.name

    def recipe_absolute_url(self):
        return f"/recipe/{self.id}/"

    def recipe_modify_url(self):
        return f"/recipe/modify/{self.id}/"


class Schedule(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    created = models.DateField(auto_now=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')

    def __str__(self):
        return self.name

    def schedule_absolute_url(self):
        return f"/plan/{self.id}/"

    def schedule_modify_url(self):
        return f"/plan/modify/{self.id}/"


class DayName(models.Model):
    name = models.CharField(max_length=16, default='Poniedziałek')
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class RecipePlan(models.Model):
    meal_name = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    order = models.CharField(max_length=126)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('order', 'day_name', 'meal_name')

        
class Page(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(max_length=128, unique=True)

    def slug(self):
        return slugify(self.title)
