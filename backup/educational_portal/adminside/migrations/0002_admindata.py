# Generated by Django 5.0.6 on 2024-06-11 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminData',
            fields=[
                ('admin_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=20)),
                ('admin_pass', models.CharField(max_length=100)),
                ('admin_email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'db_table': 'AdminData',
            },
        ),
    ]
