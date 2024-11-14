# Generated by Django 5.0.7 on 2024-11-14 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0073_materials_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admindata',
            name='admin_pass',
            field=models.CharField(blank=True, default='123456', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='faculties',
            name='fac_password',
            field=models.CharField(blank=True, default='12345678', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='stud_guardian_password',
            field=models.CharField(blank=True, default='123456', max_length=400, null=True),
        ),
    ]
