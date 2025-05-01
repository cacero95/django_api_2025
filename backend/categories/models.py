from django.db import models
from autoslug import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'