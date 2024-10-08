# Generated by Django 4.2.9 on 2024-08-04 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0028_rename_guarantor_loanguarantor'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanamortization',
            name='interest_balance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loanamortization',
            name='principal_balance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='PenaltyPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.loan')),
            ],
        ),
    ]
