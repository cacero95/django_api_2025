# Generated by Django 5.2 on 2025-04-11 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='create_date',
            new_name='created_date',
        ),
    ]
