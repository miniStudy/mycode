# Generated by Django 5.0.6 on 2024-08-02 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0009_delete_cheque_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque_Collection',
            fields=[
                ('cheque_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cheque_number', models.IntegerField()),
                ('cheque_bounce', models.BooleanField(default=False)),
                ('cheque_date', models.DateField()),
                ('cheque_expiry', models.DateField()),
                ('cheque_paid', models.BooleanField(default=False)),
                ('cheque_stud_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.students')),
            ],
            options={
                'db_table': 'cheque_Collection',
            },
        ),
    ]
