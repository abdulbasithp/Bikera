# Generated by Django 4.0.4 on 2022-06-03 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='slug',
        ),
    ]