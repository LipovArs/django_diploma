# Generated by Django 3.2.12 on 2024-01-10 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='assignner',
            new_name='assigner',
        ),
    ]
