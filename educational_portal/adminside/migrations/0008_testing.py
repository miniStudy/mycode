# Generated by Django 5.0.6 on 2024-07-08 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0007_inquiries'),
    ]

    operations = [
        migrations.CreateModel(
            name='testing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testing_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Testing',
            },
        ),
    ]
