# Generated by Django 5.0.7 on 2024-10-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0044_alter_mail_variables_mail_variables_mail_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail_templates',
            name='mail_temp_type',
            field=models.CharField(choices=[('Itroduction_mail', 'Itroduction_mail'), ('Marketing_mail', 'Marketing_mail'), ('Announcement_mail', 'Announcement_mail')], max_length=50),
        ),
    ]
