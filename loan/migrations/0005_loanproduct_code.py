# Generated by Django 4.2.7 on 2024-02-26 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_loan_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanproduct',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]