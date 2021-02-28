from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
import time
# import datetime
from datetime import timedelta
from mainapp.models import Exam, Institute
from django.core.mail import EmailMessage


# This is the function you want to schedule - add as many as you want and then register them in the start() function below
# def send_reminders():
#     today = timezone.now()
#     tomorrow = timezone.now() + timedelta(days=1)
#     obj  = Exam.objects.filter(date__lte = tomorrow, date__gte=today)
#     for i in obj:
#         exam = Exam.objects.get(id=i.id)
#         obj = exam.student.all()
#         emails = []
#         for o in obj:
#              emails.append(o.email)
#         print(emails)
#         mail_subject = 'Get Ready for your Exam!!'
#         message = f'{exam.name} is within 24 hrs. Please check out the link for more info /http://127.0.0.1:8000/view_exam/{exam.id}'

#         email = EmailMessage(
#             mail_subject, message, to= emails
#         )
#         email.send()


# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     # run this job every 24 hours
#     scheduler.add_job(send_reminders, 'interval', hours=24, name='send_reminders', jobstore='default')
#     register_events(scheduler)
#     scheduler.start()
#     print("Scheduler started...", file=sys.stdout)