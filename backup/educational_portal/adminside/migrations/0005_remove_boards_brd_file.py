# Generated by Django 5.0.6 on 2024-06-18 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0004_boards_brd_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boards',
            name='brd_file',
        ),
    ]
