# Generated by Django 4.2.9 on 2024-10-06 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientApp', '0009_alter_person_account_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='land_mark',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]