# Generated by Django 4.0.2 on 2022-03-01 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_network_alter_tvshow_network'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvshow',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
