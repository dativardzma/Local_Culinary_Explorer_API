# Generated by Django 5.1.7 on 2025-03-14 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_dish_images_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='creator',
        ),
    ]
