# Generated by Django 4.2.9 on 2024-08-05 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientApp', '0007_alter_person_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='account_balance',
            field=models.FloatField(default=0),
        ),
    ]
