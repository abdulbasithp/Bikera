# Generated by Django 4.0.4 on 2022-06-01 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_image1_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image4',
        ),
    ]
