# Generated by Django 5.1.1 on 2024-10-21 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Image_Effects_handler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimages',
            name='image',
            field=models.URLField(blank=True),
        ),
    ]