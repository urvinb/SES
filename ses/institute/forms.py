from django import forms
from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
import bcrypt
import datetime


from mainapp.models import Institute, Exam

class InstituteModelForm(forms.ModelForm):
    password = forms.CharField(
        min_length=8, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        min_length=8, label='Confirm Password', widget=forms.PasswordInput(attrs = {'class': 'input100', 'placeholder':'Confirm Password'}))
    email = forms.EmailField(max_length=200)

    class Meta:
        model = Institute
        fields = [
            'name',
            'email',
            'address',
            'contact',
            'domain',
            'region',
            'password'
        ]
        widgets={}
        

    def __init__(self, *args, **kwargs):
        super(InstituteModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'input100','placeholder': 'Institute Name'})
        self.fields['address'].widget= forms.TextInput(attrs = {'class': 'input100', 'placeholder':'Address'})
        self.fields['email'].widget = forms.EmailInput(attrs = {'class': 'input100', 'placeholder':'Email'})
        self.fields['contact'].widget=forms.TextInput(attrs = {'class': 'input100', 'placeholder':'Contact'})
        self.fields['domain'].widget=forms.TextInput(attrs = {'class': 'input100', 'placeholder':'Domain'})
        self.fields['region'].widget = forms.TextInput(attrs = {'class': 'input100', 'placeholder':'Region'})
        self.fields['password'].widget = forms.PasswordInput(attrs = {'class': 'input100', 'placeholder':'Password'})


        
    def clean_contact(self):
        phoneno = self.cleaned_data['contact']
        if(len(phoneno) != 10):
            print("wrong phone")
            raise forms.ValidationError("""Enter a valid phone number""")
        return phoneno

    
    def clean_email(self):
        emailid = self.cleaned_data['email']
        if emailid and Institute.objects.filter(email=emailid).exists():
            raise forms.ValidationError(
                """Emailid already exist""", code='email')
        return emailid

    def clean(self):
        cleaned_data = super().clean()
        password_one = self.cleaned_data['password']
        hash_password = bcrypt.hashpw(password_one.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        password_two = self.cleaned_data['password2']

        RegexLength = re.compile(r'^\S{8,}$')
        RegexDigit = re.compile(r'\d')
        RegexLower = re.compile(r'[a-z]')
        RegexUpper = re.compile(r'[A-Z]')

        if (password_one != password_two):
            raise forms.ValidationError(
                """Password and Confirm Password did not match""", code='password')
        else:
            if RegexLength.search(password_one) == None or RegexDigit.search(password_one) == None or RegexUpper.search(password_one) == None or RegexLower.search(password_one) == None:
                raise forms.ValidationError(
                    """Enter a strong password""", code='password')

        cleaned_data['password'] = hash_password

        return cleaned_data


class Institute_LoginForm(forms.Form):

    email = forms.EmailField(label='', max_length=100, widget= forms.TextInput(attrs = {'class': 'input100', 'placeholder':'Email'}))
    password = forms.CharField(
        min_length=8, label='', widget=forms.PasswordInput(attrs = {'class': 'input100', 'placeholder':'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        emailid = cleaned_data['email']
        spassword = cleaned_data['password']

        if emailid and Institute.objects.filter(email=emailid).exists():
            obj = Institute.objects.get(email=emailid)
        else:
            raise ValidationError("""Email Id is not registered..""")

        if not bcrypt.checkpw(spassword.encode('utf-8'), obj.password.encode('utf-8')):
            raise ValidationError("""Incorrect Password""")

        return cleaned_data

class ExamModelForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = [
            'name',
            'reg_link',
            'date',
            'time',
            'duration',
            'medium',
            'degree',
            'last_day_register',
            'rules_pdf',
            'syllabus_pdf',
            'marking_scheme',
            'extra_details',
        ]

        widgets = {}
                 
    def __init__(self, *args, **kwargs):
        CHOICES = [('Online', 'Online'), ('Offline', 'Offline')]
        super(ExamModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'input--style-1','placeholder': 'Exam Name', 'label': 'Exam Name'})
        self.fields['reg_link'].widget= forms.URLInput(attrs = {'class': 'input--style-1', 'placeholder':'Registration Link'})
        self.fields['date'].widget=forms.DateInput(attrs = {'type':'date','class': 'input--style-1'})
        self.fields['time'].widget=forms.TimeInput(attrs = {'class': 'input--style-1'})
        self.fields['duration'].widget=forms.NumberInput(attrs = {'min':1, 'class': 'input--style-1'})
        self.fields['rules_pdf'].widget = forms.FileInput(attrs = {'class': 'input--style-1'})
        self.fields['syllabus_pdf'].widget = forms.FileInput(attrs = {'class': 'input--style-1'})
        self.fields['marking_scheme'].widget = forms.FileInput(attrs = {'class': 'input--style-1'})
        self.fields['extra_details'].widget = forms.Textarea(attrs = {'class': 'input--style-1','rows': 6, 'placeholder':'Additional Details'})
        self.fields['last_day_register'].widget = forms.DateInput(attrs = {'type':'date', 'class': 'input--style-1 js-datepicker'})



