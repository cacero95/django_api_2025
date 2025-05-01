from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=100, null=False)
    created_date = models.DateTimeField()
    update_date = models.DateTimeField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'contact'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'