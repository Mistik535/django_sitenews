# Generated by Django 4.2.1 on 2023-12-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_news_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='is_published',
            field=models.BooleanField(choices=[(False, 'Не опубликовано'), (True, 'Опубликовано')], default=0, verbose_name='Статус'),
        ),
    ]
