# Generated by Django 5.1.1 on 2024-10-15 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0024_announcements_domain_name_attendance_domain_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewInstitution',
            fields=[
                ('institute_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('institute_name', models.CharField(max_length=155)),
                ('institute_email', models.EmailField(max_length=254, unique=True)),
                ('institute_contact', models.CharField(max_length=15)),
                ('institute_logo', models.ImageField(upload_to='institution_logos/')),
                ('institute_domain', models.CharField(max_length=155, unique=True)),
            ],
            options={
                'db_table': 'NewInstitution',
            },
        ),
    ]