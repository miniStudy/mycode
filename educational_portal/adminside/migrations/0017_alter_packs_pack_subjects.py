# Generated by Django 5.1.1 on 2024-10-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0016_alter_students_stud_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packs',
            name='pack_subjects',
            field=models.ManyToManyField(blank=True, related_name='pack_subject', to='adminside.subject'),
        ),
    ]