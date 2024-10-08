# Generated by Django 5.0.1 on 2024-02-25 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
                ('nin', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('dob', models.DateField(blank=True, default=None, null=True)),
                ('business', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('address', models.CharField(max_length=200)),
                ('number_of_children', models.IntegerField(blank=True, default=0, null=True)),
                ('marital_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('W', 'Widowed')], default='S', max_length=1)),
                ('spouse_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('spouse_phone', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
