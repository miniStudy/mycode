from django.utils import timezone  # Correct import for timezone
from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail

# class MonthlyEmailCronJob(CronJobBase):
#     RUN_AT_TIMES = ['16:39']  # Midnight

#     schedule = Schedule(run_at_times=RUN_AT_TIMES)
#     code = 'adminside.monthly_email_cron'  # a unique code

#     def do(self):
#         if timezone.now().day == 7:
#             print('hello wolrd')
#             email_from = 'miniStudy <mail@ministudy.in>'
#             send_mail(
#                 'Monthly Email',
#                 'This is your monthly email.',
#                 email_from,
#                 ['mail.trushalpatel@gmail.com'],
#             )

def my_scheduled_job():
  print("hello world")            