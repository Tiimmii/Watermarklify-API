# Generated by Django 5.1.1 on 2024-10-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Image_Effects_handler', '0006_alter_userimages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimages',
            name='image',
            field=models.ImageField(blank=True, upload_to='WATERMARKLIFY_IMAGES/'),
        ),
    ]
