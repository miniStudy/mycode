# Generated by Django 5.0.7 on 2024-08-13 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='sub_name',
            field=models.CharField(max_length=50),
        ),
    ]
