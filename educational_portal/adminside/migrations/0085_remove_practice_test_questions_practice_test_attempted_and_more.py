# Generated by Django 5.0.7 on 2024-11-27 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0084_study_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice_test_questions',
            name='practice_test_attempted',
        ),
        migrations.CreateModel(
            name='practiceTestAttempted',
            fields=[
                ('pta_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('practice_test_attempted', models.CharField(choices=[('Attemped', 'Attemped'), ('Not_attemped', 'Not_attemped'), ('Answered', 'Answered'), ('Not_answered', 'Not_answered')], max_length=50)),
                ('pta_answer', models.TextField()),
                ('practice_test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.practice_test_questions')),
                ('pta_student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.students')),
            ],
            options={
                'db_table': 'practiceTestAttempted',
            },
        ),
    ]
