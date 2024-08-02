# Generated by Django 5.0.6 on 2024-08-02 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0012_delete_cheque_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque_Collection',
            fields=[
                ('cheque_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cheque_amount', models.FloatField()),
                ('cheque_number', models.IntegerField()),
                ('cheque_bounce', models.BooleanField(default=False)),
                ('cheque_date', models.DateField()),
                ('cheque_expiry', models.DateField(blank=True, null=True)),
                ('cheque_paid', models.BooleanField(default=False)),
                ('cheque_stud_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.students')),
            ],
            options={
                'db_table': 'Cheque_Collection',
            },
        ),
    ]
