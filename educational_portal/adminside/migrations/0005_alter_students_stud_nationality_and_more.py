# Generated by Django 5.0.6 on 2024-08-13 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0004_alter_students_stud_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='stud_nationality',
            field=models.CharField(blank=True, default='India', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='stud_pass',
            field=models.TextField(blank=True, default='12345678', null=True),
        ),
        migrations.CreateModel(
            name='Today_Teaching',
            fields=[
                ('today_teaching_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('today_teaching_desc', models.CharField(max_length=600)),
                ('today_teaching_date', models.DateTimeField(auto_now_add=True)),
                ('today_teaching_chap_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.chepter')),
                ('today_teaching_fac_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.faculties')),
            ],
            options={
                'db_table': 'Today_Teaching',
            },
        ),
    ]
