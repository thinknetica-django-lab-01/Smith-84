# Generated by Django 3.0 on 2021-01-30 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='slug',
            field=models.SlugField(blank=True, primary_key=True, serialize=False),
        ),
    ]
