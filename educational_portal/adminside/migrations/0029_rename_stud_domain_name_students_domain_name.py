# Generated by Django 5.1.2 on 2024-10-18 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0028_rename_domain_name_students_stud_domain_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='students',
            old_name='stud_domain_name',
            new_name='domain_name',
        ),
    ]