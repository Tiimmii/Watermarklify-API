# Generated by Django 5.1.1 on 2024-10-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Image_Effects_handler', '0003_rename_image_userimages_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimages',
            name='name',
            field=models.CharField(default='ghost', max_length=100),
        ),
    ]
