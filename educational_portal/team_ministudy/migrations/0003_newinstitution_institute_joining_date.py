# Generated by Django 5.1.2 on 2024-10-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_ministudy', '0002_newinstitution_institute_lock'),
    ]

    operations = [
        migrations.AddField(
            model_name='newinstitution',
            name='institute_joining_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]