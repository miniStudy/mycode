# Generated by Django 5.0.7 on 2024-11-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0090_teacher_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher_review',
            name='domain_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]