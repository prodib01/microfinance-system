# Generated by Django 4.2.9 on 2024-07-03 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientApp', '0007_alter_person_options'),
        ('loan', '0024_remove_loan_guarantors_loan_guarantor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='guarantor',
        ),
        migrations.AddField(
            model_name='loan',
            name='guarantors',
            field=models.ManyToManyField(related_name='loans', to='clientApp.person'),
        ),
    ]
