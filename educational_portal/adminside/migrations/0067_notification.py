# Generated by Django 5.0.7 on 2024-11-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0066_merge_20241112_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notify_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('notify_title', models.TextField(max_length=155)),
                ('notify_notification', models.TextField(max_length=255)),
                ('notify_date', models.DateField(auto_now_add=True)),
                ('domain_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'Notification',
            },
        ),
    ]
