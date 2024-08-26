# Generated by Django 4.2.9 on 2024-08-26 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0044_alter_systemparameters_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='deposit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='loan.deposit'),
        ),
    ]
