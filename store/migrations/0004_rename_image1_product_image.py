# Generated by Django 4.0.4 on 2022-06-01 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_image2_alter_product_image3_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image1',
            new_name='image',
        ),
    ]
