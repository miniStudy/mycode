# Generated by Django 5.0.7 on 2024-11-20 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0077_admimlead'),
    ]

    operations = [
        migrations.AddField(
            model_name='admimlead',
            name='domain_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]