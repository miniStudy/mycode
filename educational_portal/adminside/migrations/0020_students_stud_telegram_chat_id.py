# Generated by Django 5.0.7 on 2024-10-08 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0019_test_attempted_users_tau_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='stud_telegram_chat_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
