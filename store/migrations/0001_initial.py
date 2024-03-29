# Generated by Django 4.0.4 on 2022-05-28 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('brand', models.CharField(choices=[('nivia', 'Nivia'), ('nike', 'Nike'), ('sega', 'Sega'), ('puma', 'Puma'), ('adidas', 'Adidas'), ('kobo', 'Kobo'), ('cosco', 'Cosco'), ('supreme', 'Supreme')], default='audi', max_length=20)),
                ('description', models.TextField(blank=True, max_length=2000)),
                ('image', models.ImageField(upload_to='images/')),
                ('slug', models.SlugField(max_length=225)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('in_stock', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-created',),
            },
        ),
    ]
