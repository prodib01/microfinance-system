# Generated by Django 4.2.7 on 2024-03-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0016_deposit_ammortization'),
    ]

    operations = [
        migrations.AddField(
            model_name='penalty',
            name='name',
            field=models.CharField(default=5, max_length=50),
            preserve_default=False,
        ),
    ]
