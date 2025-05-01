from django.db import models
from autoslug import AutoSlugField
from categories.models import Category
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    # DO_NOTHING related many to many
    user = models.ForeignKey(User, models.DO_NOTHING)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    name = models.CharField(max_length=100, null=False)
    slug = AutoSlugField(populate_from='name', max_length=100)
    time = models.CharField(max_length=100, null=True)
    image = models.CharField(max_length=100, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'recipes'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'