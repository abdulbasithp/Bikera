# Generated by Django 4.0.4 on 2022-06-03 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_image1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
