# Generated by Django 5.1.1 on 2024-10-04 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0017_alter_packs_pack_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='stud_pack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='adminside.packs'),
        ),
    ]