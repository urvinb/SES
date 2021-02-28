from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .tokens import account_activation_token
from django.db import connection
from django.template.loader import render_to_string

from itertools import chain
from .forms import *
from mainapp.models import Institute

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
# from django_email_verification import sendConfirm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from random import randint

from .decorators import is_institute, is_loggedin


# Create your views here.
def login(request):
    if 'user_email' in request.session:
        print(request.session['user_email'])
        print(request.session['user_role'])
        return redirect('index_institute')
    if request.method == "POST":
        login_form = Institute_LoginForm(request.POST)
        if login_form.is_valid():
            print(login_form['email'].value())
            obj = Institute.objects.get(
                email=login_form['email'].value())
            if obj.is_email_active:
                request.session['user_email'] = login_form['email'].value()
                request.session['user_role'] = 'institute'
                print(request.session['user_email'])
                print(request.session['user_role'])
                return redirect('index_institute')
            else:
                e = "Your Email is not verified yet. Verify it to continue Login"
            return render(request, "institute/login.html", {'inst_login': login_form ,'e':e})

        else:
            inst_login = {'form': login_form}
            e = "Invalid email/password."
            return render(request, "institute/login.html", {'inst_login': inst_login,'e':e})

    else:
        form = Institute_LoginForm(request.POST or None)
        inst_login = {'form': form}
        errors = ''
        return render(request, "institute/login.html", {'inst_login': inst_login})


def register(request):
    if request.method == "POST":
        sform = InstituteModelForm(request.POST)
        
        if sform.is_valid():
            
            del sform.fields['password2']
            obj = sform.save()
            current_site = get_current_site(request)
            mail_subject = 'Verify your Institute account.'
            message = render_to_string('institute/activate.html', {
                'user': obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
                'token': account_activation_token.make_token(obj),
            })
            to_email = obj.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request,f'You have successfully registered.')
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            
            inst = {'form': sform}
            e='This email address is already in use.Try again with a new one.'
            return render(request, "institute/register.html", {'inst': inst,'e':e})
    else:
        form = InstituteModelForm(request.POST or None)
        inst = {'form': form}
        errors = ''
        return render(request, "institute/register.html", {'inst': inst})

@is_loggedin
@is_institute
def logout(request):
    try:
        del request.session['user_email']
        if 'user_role' in request.session:
            del request.session['user_role']
        return HttpResponse('Logged out successfully')
        # return render(request, "institute/login.html", {'inst_login': inst_login})
    except:
        return HttpResponse('Some error occured..Try again later')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Institute.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Institute.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_active = True
        user.save()
        print("user registered")
        site = get_current_site(request)
        print(site)
        request.session['user_email'] = user.email
        return HttpResponse('Thank you for your email confirmation. You can now login!!')
    else:
        return HttpResponse('Activation link is invalid!')


@is_loggedin
@is_institute
def examform(request):
    if request.method == "POST":
        eform = ExamModelForm(request.POST, request.FILES)
        inst_obj = Institute.objects.get(email=request.session['user_email'])
        if eform.is_valid():
            obj = eform.save(commit=False)
            obj.institute = Institute.objects.get(
                email=request.session['user_email'])
            obj.save()
            send_mail_on_add(obj.id)
            return redirect('index_institute')
        else:
            print("no hello")
            exam = {'form': eform}
            messages.error(request, "Error")
            return render(request, "institute/examform.html", {'exam': exam})
    else:
        eform = ExamModelForm(request.POST, request.FILES)
        exam = {'form': eform}
        errors = ''
        return render(request, "institute/examform.html", {'exam': exam})


@is_loggedin
@is_institute
def index_institute(request):
    obj = Institute.objects.get(email=request.session['user_email'])
    exam_obj = Exam.objects.filter(institute=obj)

    if 'search_form' in request.POST:
        institute_obj = Institute.objects.get(email=request.session['user_email'])
        keyword=request.POST.get("universal_search")
        print(keyword)
        name_objs = exam_obj.filter(name__contains=keyword)
        medium_objs = exam_obj.filter(medium__contains=keyword)
        exam_search_obj =set(chain(name_objs,medium_objs))
        print(exam_search_obj)

        context =  {
        'obj':obj,
        'exam_obj':exam_search_obj
        }
        return render(request, "institute/index.html",context)        

    context = {
        'obj':obj,
        'exam_obj':exam_obj
    }
    return render(request, "institute/index.html",context)

@is_loggedin
@is_institute
def delete_exam(request, id):
    exam_id = id
    obj = Exam.objects.get(id=exam_id)
    if obj.institute.email != request.session['user_email']:
        raise PermissionDenied
    obj.delete()
    return redirect('index_institute')


@is_loggedin
@is_institute
def update_exam(request, id):
    exam_id = id
    obj = Exam.objects.get(id=exam_id)
    if obj.institute.email != request.session['user_email']:
        raise PermissionDenied
    if request.method == 'POST':
        edit_form = ExamModelForm(request.POST, request.FILES)
        if edit_form.is_valid():
            obj.name = edit_form.cleaned_data['name']
            obj.date = edit_form.cleaned_data['date']
            obj.time = edit_form.cleaned_data['time']
            obj.duration = edit_form.cleaned_data['duration']
            obj.reg_link = edit_form.cleaned_data['reg_link']
            if(edit_form.cleaned_data['rules_pdf']):
                obj.rules_pdf = edit_form.cleaned_data['rules_pdf']
            if(edit_form.cleaned_data['syllabus_pdf']):
                obj.syllabus_pdf = edit_form.cleaned_data['syllabus_pdf']
            if(edit_form.cleaned_data['marking_scheme']):
                obj.marking_scheme = edit_form.cleaned_data['marking_scheme']
            if(edit_form.cleaned_data['degree']):
                obj.degree = edit_form.cleaned_data['degree']
            if(edit_form.cleaned_data['medium']):
                obj.degree = edit_form.cleaned_data['medium']
            if(edit_form.cleaned_data['extra_details']):
                obj.extra_details = edit_form.cleaned_data['extra_details']
            # obj1 = edit_form.save(commit=False) 
            # obj1.institute = Institute.objects.get(
            #     email=request.session['user_email'])
            # print("hello", obj1, obj1.institute, obj1.date)
            obj.save()
            print("heyyyyyy")
            send_mail_on_update_of_exam(id)
            return redirect('../')
        else:
            exam = {
                'form': edit_form
            }
            return render(request, 'institute/update_examform.html', {'exam': exam})
    else:

        edit_form = ExamModelForm(instance=obj)
        exam = {
            'form': edit_form
        }
        errors = ''
        return render(request, 'institute/update_examform.html', {'exam': exam})


def send_mail_on_update_of_exam(id):
    exam = Exam.objects.get(id=id)
    obj = exam.student.all()
    emails = []
    for o in obj:
        emails.append(o.email)
    print(emails)
    mail_subject = 'Exam Details Updated!!'
    message = f'{exam.name} exam has been updated. Please check out the link for more info /http://127.0.0.1:8000/view_exam/{exam.id}'

    email = EmailMessage(
        mail_subject, message, to= emails
    )
    email.send()

def send_mail_on_add(id):
    exam = Exam.objects.get(id=id)
    ins = exam.institute
    obj = ins.student.all()
    emails = []
    for o in obj:
        emails.append(o.email)
    print(emails)
    mail_subject = 'New Exam Added By ' + ins.name
    message = f'{exam.name} exam has been added. Please check out the link for more info /http://127.0.0.1:8000/view_exam/{exam.id}'
    email = EmailMessage(
        mail_subject, message, to= emails
    )
    email.send()

