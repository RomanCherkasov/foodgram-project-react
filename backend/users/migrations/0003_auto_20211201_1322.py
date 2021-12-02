# Generated by Django 3.2.9 on 2021-12-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211201_1322'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='uniq_follow',
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='uniq_subscribe'),
        ),
    ]
