# Generated by Django 3.2.9 on 2021-11-18 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_delete_issubscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='measurement_unit',
            field=models.CharField(max_length=10, null=True),
        ),
    ]