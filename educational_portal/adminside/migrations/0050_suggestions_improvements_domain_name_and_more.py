# Generated by Django 5.0.7 on 2024-11-05 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0049_suggestions_improvements_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestions_improvements',
            name='domain_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterModelTable(
            name='suggestions_improvements',
            table='suggestions_improvements',
        ),
    ]
