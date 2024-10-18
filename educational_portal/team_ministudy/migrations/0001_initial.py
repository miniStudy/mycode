# Generated by Django 5.1.2 on 2024-10-16 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminside', '0026_delete_newinstitution'),
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
        migrations.CreateModel(
            name='MinistudyPayment',
            fields=[
                ('ministudypay_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ministudypay_amount', models.IntegerField()),
                ('ministudypay_paid', models.BooleanField(default=False)),
                ('ministudypay_student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.students')),
            ],
            options={
                'db_table': 'MinistudyPayment',
            },
        ),
    ]