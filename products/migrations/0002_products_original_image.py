# Generated by Django 3.2.13 on 2022-11-01 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='original_image',
            field=models.ImageField(default=0, upload_to='photos'),
            preserve_default=False,
        ),
    ]
