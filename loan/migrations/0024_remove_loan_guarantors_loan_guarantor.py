# Generated by Django 4.2.9 on 2024-07-03 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientApp', '0007_alter_person_options'),
        ('loan', '0023_remove_loan_guarantor_loan_guarantors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='guarantors',
        ),
        migrations.AddField(
            model_name='loan',
            name='guarantor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guarantor', to='clientApp.person'),
        ),
    ]