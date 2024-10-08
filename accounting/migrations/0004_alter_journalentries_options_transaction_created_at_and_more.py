# Generated by Django 4.2.9 on 2024-08-24 16:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_rename_note_transaction_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journalentries',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Journal Entries'},
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
