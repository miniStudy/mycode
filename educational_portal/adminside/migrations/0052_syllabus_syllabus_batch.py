# Generated by Django 5.0.7 on 2024-11-05 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0051_delete_suggestions_improvements'),
    ]

    operations = [
        migrations.AddField(
            model_name='syllabus',
            name='syllabus_batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminside.batches'),
        ),
    ]
