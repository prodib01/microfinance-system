# Generated by Django 4.2.9 on 2024-08-20 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0036_alter_systemparameters_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Penalty',
        ),
    ]
