# Generated by Django 5.0.7 on 2024-11-05 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0048_merge_20241105_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='stude_created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='mail_templates',
            name='mail_temp_type',
            field=models.CharField(choices=[('Itroduction_mail', 'Itroduction_mail'), ('Marketing_mail', 'Marketing_mail'), ('Announcement_mail', 'Announcement_mail'), ('Attendance_mail', 'Attendance_mail'), ('Cheque_mail', 'Cheque_mail'), ('Cheque_update_mail', 'Cheque_update_mail'), ('Faculty_mail', 'Faculty_mail'), ('Institute_mail', 'Institute_mail'), ('Parent_meeting_mail', 'Parent_meeting_mail'), ('Payment_mail', 'Payment_mail'), ('Student_mail', 'Student_mail'), ('Timetable_mail', 'Timetable_mail')], max_length=50),
        ),
    ]
