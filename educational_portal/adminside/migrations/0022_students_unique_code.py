# Generated by Django 5.0.7 on 2024-10-09 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0021_rename_stud_telegram_chat_id_students_stud_telegram_parentschat_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='unique_code',
            field=models.CharField(blank=True, editable=False, max_length=20),
        ),
    ]
