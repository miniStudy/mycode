# Generated by Django 5.0.7 on 2024-11-28 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0091_teacher_review_domain_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teacher_review',
            unique_together=set(),
        ),
    ]
