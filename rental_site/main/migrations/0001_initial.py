# Generated by Django 3.0 on 2021-01-23 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField()),
                ('description', models.CharField(default=None, max_length=255)),
                ('address', models.CharField(default=None, max_length=200)),
                ('action', models.CharField(choices=[('Продажа', 'Продажа'), ('Аренда', 'Аренда'), ('Посуточно', 'Посуточно')], max_length=20)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('apartment', 'room', 'garage', 'landplot')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_square', models.FloatField(default=True)),
                ('floor', models.PositiveSmallIntegerField()),
                ('number_of_rooms', models.PositiveSmallIntegerField()),
                ('kitchen_square', models.FloatField()),
                ('living_square', models.FloatField()),
            ],
            options={
                'verbose_name': 'Квартира',
                'verbose_name_plural': 'Квартиры',
            },
        ),
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_square', models.FloatField(default=True)),
                ('number_of_floors', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Гараж',
                'verbose_name_plural': 'Гаражы',
            },
        ),
        migrations.CreateModel(
            name='LandPlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_square', models.FloatField(default=True)),
            ],
            options={
                'verbose_name': 'Земельный участок',
                'verbose_name_plural': 'Земельные участки',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Населенный пункт',
                'verbose_name_plural': 'Населенные пункты',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_square', models.FloatField(default=True)),
                ('floor', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(default=True, max_length=12, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image_folder', verbose_name='Изображение')),
                ('ad', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='main.Ad')),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Region'),
        ),
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
