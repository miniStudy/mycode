# Generated by Django 5.0.6 on 2024-07-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0010_alter_test_attempted_users_tau_correct_ans_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chepterwise_test',
            name='test_time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='test_attempted_users',
            name='tau_completion_time',
            field=models.CharField(max_length=200),
        ),
    ]
