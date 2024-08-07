# Generated by Django 4.2.9 on 2024-07-02 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientApp', '0007_alter_person_options'),
        ('loan', '0020_alter_document_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='guarantor',
        ),
        migrations.AddField(
            model_name='loan',
            name='guarantor',
            field=models.ManyToManyField(related_name='guarantors', to='clientApp.person'),
        ),
    ]
