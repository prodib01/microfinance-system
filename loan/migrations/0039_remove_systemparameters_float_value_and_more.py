# Generated by Django 4.2.9 on 2024-08-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0038_rename_deposit_deposit_amount_deposited'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemparameters',
            name='float_value',
        ),
        migrations.AddField(
            model_name='systemparameters',
            name='decimal_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
