from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# Create your models here
class Institute(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=20,blank=True)
    domain = models.CharField(max_length=50)
    region = models.CharField(max_length=20,blank=True,default='')
    created = models.DateTimeField(default=timezone.now)
    student = models.ManyToManyField(User,blank=True)
    is_email_active = models.BooleanField(default=True)
    password = models.CharField(max_length=250, blank = True)

    def __str__(self):
        return f'{self.name}'
    
    def get_is_subscribed(self,user):
        objs = self.student.all()
        for obj in objs:
            if obj == user:
                return True
        return False


exam_type = [
    ("Online", "Online"),
    ("Offline", "Offline"),
]


class Exam(models.Model):
    name = models.CharField(max_length=500)
    reg_link = models.CharField(max_length=2000)
    date = models.DateField(blank = True, default=timezone.now())
    time = models.TimeField(blank=True,default='20:00')
    duration = models.IntegerField(default=0, blank= True)
    medium = models.CharField(max_length=10, choices=exam_type)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    rules_pdf = models.FileField(upload_to='uploads/',blank=True)
    syllabus_pdf = models.FileField(upload_to='uploads/',blank=True)
    marking_scheme = models.FileField(upload_to='uploads/',blank=True)
    extra_details = models.CharField(blank=True, max_length=2000)
    student = models.ManyToManyField(User,blank=True)
    is_govt = models.BooleanField(default=False)
    last_day_register = models.DateField(default=timezone.now())
    degree = models.CharField(max_length=20,default='-')
    youtube_link = models.CharField(max_length=2000,blank=True)
    youtube_link2 = models.CharField(max_length=2000,blank=True)
    youtube_link3 = models.CharField(max_length=2000,blank=True)


    def save(self, *args, **kwargs):
        super(Exam, self).save(*args, **kwargs)
        # print('Did this attribute update? (attr):', self.attr)
        print('Save method executed!')

    def get_left_days(self):
            delta =  self.date - timezone.now().date() 
            return delta.days

    def __str__(self):
        return f'{self.name}  {self.degree}'

    def get_is_subscribed(self,user):
        objs = self.student.all()
        for obj in objs:
            if obj == user:
                return True
        return False


