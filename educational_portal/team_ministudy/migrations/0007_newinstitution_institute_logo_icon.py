# Generated by Django 5.0.7 on 2024-11-22 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_ministudy', '0006_distributer_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='newinstitution',
            name='institute_logo_icon',
            field=models.ImageField(default=1, upload_to='institution_logos/'),
            preserve_default=False,
        ),
    ]
