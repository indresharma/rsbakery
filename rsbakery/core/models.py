from django.db import models
from django.conf import settings
from django.urls import reverse

from .utils import crop_and_save

class CarouselObjects(models.Model):
    img = models.ImageField(upload_to='pictures')
    img_text = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = crop_and_save(self.img.path, 600, 1200)
        image.save(self.img.path)
        

class Tags(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Ingredients'


class Recipe(models.Model):
    UNIT_CHOICES = (
        ('teaspoon', 'Teaspoon'),
        ('tablespoon', 'Tablespoon'),
        ('unit', 'Unit'),
        ('add_to_taste', 'Add to taste'),
    )

    title = models.CharField(max_length=200)
    data_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, blank=True)
    ingredients = models.ManyToManyField(Ingredients, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='pictures', default='pictures/mypic.jpg')
    preparation_time = models.IntegerField(blank=True, null=True)
    calories = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    paid_recipe = models.BooleanField(default=False)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='unit')
    qty = models.IntegerField(blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = crop_and_save(self.image.path, 350, 400)
        image.save(self.image.path)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:detail', args=[self.pk])

    def get_summary(self):
        return self.description[:100] + '...'

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '/media/pictures/mypic.jpg'

    @property
    def comments(self):
        qs = Comments.objects.filter(recipe=self).order_by('-created')
        return qs

    def likes_count(self):
        return self.likes.all().count()

    
class RecipeCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.user.profile.first_name


class Comments(models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
