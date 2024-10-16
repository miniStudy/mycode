# Generated by Django 5.0.7 on 2024-09-12 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0014_question_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquiries',
            name='inq_subjects',
        ),
        migrations.AddField(
            model_name='inquiries',
            name='stud_nationality',
            field=models.CharField(blank=True, default='India', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inquiries',
            name='stud_pack',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminside.packs'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='students',
            name='stud_username',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
