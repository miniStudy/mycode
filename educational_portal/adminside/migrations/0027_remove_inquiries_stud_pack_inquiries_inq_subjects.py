# Generated by Django 5.1.2 on 2024-10-16 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0026_delete_newinstitution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquiries',
            name='stud_pack',
        ),
        migrations.AddField(
            model_name='inquiries',
            name='inq_subjects',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
