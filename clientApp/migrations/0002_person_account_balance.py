# Generated by Django 4.2.7 on 2024-02-26 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='account_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]