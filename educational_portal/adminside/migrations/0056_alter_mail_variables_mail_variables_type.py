# Generated by Django 5.0.7 on 2024-11-08 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0055_remove_mail_variables_mail_variables_mail_template_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail_variables',
            name='mail_variables_type',
            field=models.CharField(blank=True, choices=[('Introduction_mail', 'Introduction_mail'), ('Marketing_mail', 'Marketing_mail'), ('Announcement_mail', 'Announcement_mail'), ('Attendance_mail', 'Attendance_mail'), ('Cheque_mail', 'Cheque_mail'), ('Cheque_update_mail', 'Cheque_update_mail'), ('Faculty_mail', 'Faculty_mail'), ('Institute_mail', 'Institute_mail'), ('Parent_meeting_mail', 'Parent_meeting_mail'), ('Payment_mail', 'Payment_mail'), ('Student_mail', 'Payment_mail'), ('Timetable_mail', 'Timetable_mail'), ('Admin_mail', 'Admin_mail'), ('Marks_mail', 'Marks_mail')], max_length=50, null=True),
        ),
    ]
