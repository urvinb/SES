from django.shortcuts import render,redirect
import pdfkit
from django.template import loader
from django.http import HttpResponse
from .models import Exam, Institute
from itertools import chain
from django.contrib import messages
from django.contrib.auth import logout
from .Data import api




# Create your views here.
def index(request):
    exam_obj = Exam.objects.all()

    df = api.world_headlines()
    df = df.head(9)
   
    if 'search_form' in request.POST:
        institute_obj = Institute.objects.all()
        keyword=request.POST.get("universal_search")
        print(keyword)
        name_objs = exam_obj.filter(name__contains=keyword)
        medium_objs = exam_obj.filter(medium__contains=keyword)
        institute_objs = exam_obj.prefetch_related('institute').filter(institute__name__contains=keyword)  
        degree_objs = exam_obj.filter(degree__contains=keyword)  

        exam_search_objects =set(chain(name_objs,medium_objs,institute_objs,degree_objs))
        print(exam_search_objects)
        context = {
            'title' : 'Smart Education System',
            'exam_obj':exam_search_objects,
            'tab':1
        }
        return  render(request,'mainapp/index.html',context)
    for obj in exam_obj:
        if obj.get_left_days() <= 0 :
            exam_obj = exam_obj.exclude(id=obj.id)

    exam_obj = exam_obj.order_by('date')[0:9]
    
    context = {
        'title' : 'Smart Education System',
        'exam_obj':exam_obj,
        'df':df,
    }
    return render(request,'mainapp/index.html',context)


def subscriptions(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    exam_obj = Exam.objects.all()
    exam_obj = exam_obj.filter(student=request.user)

    context = {
        'title' : 'My Subscriptions',
        'exam_obj':exam_obj
    }

    return render(request,'mainapp/subscribed.html',context)
    
def domains(request,id):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    exam_obj = Exam.objects.all()
    # eng_exam_obj = exam_obj.prefetch_related('institute').filter(institute__domain='Engineering')
    gov_obj = exam_obj.filter(is_govt=True)
    private_obj = exam_obj.filter(is_govt=False)
    if id==0:
        context = {
            'title' : 'Government',
            'exam_obj': gov_obj
        }
        if 'filter' in request.POST:
            domain=request.POST.get("domain")
            state=request.POST.get("inputState")
            institute=request.POST.get("institute")
            domain_obj_filter = gov_obj.prefetch_related('institute').filter(institute__domain=domain)
            state_obj_filter = gov_obj.prefetch_related('institute').filter(institute__region=state)
            institute_obj = gov_obj.prefetch_related('institute').filter(institute__name=institute)
            filter_objects =set(chain(domain_obj_filter,state_obj_filter,institute_obj))
            context = {
                'title' : 'Government',
                'exam_obj': filter_objects
            }

    if id==1:
        context = {
            'title' : 'Private',
            'exam_obj': private_obj
        }
    
        if 'filter' in request.POST:
            domain=request.POST.get("domain")
            state=request.POST.get("inputState")
            institute=request.POST.get("institute")
            domain_obj_filter = private_obj.prefetch_related('institute').filter(institute__domain=domain)
            state_obj_filter = private_obj.prefetch_related('institute').filter(institute__region=state)
            institute_obj = private_obj.prefetch_related('institute').filter(institute__name=institute)
            filter_objects =set(chain(domain_obj_filter,state_obj_filter,institute_obj))
            context = {
                'title' : 'Private',
                'exam_obj': filter_objects
            }

    return render(request,'mainapp/domainwise.html',context)


def view_exam(request,id):
    obj = Exam.objects.get(id=id)
    students = obj.student.all()    
    youtube_obj = []
    if obj.youtube_link:
        youtube_obj.append(obj)
    if obj.youtube_link2:
        youtube_obj.append(obj)
    if obj.youtube_link3:
        youtube_obj.append(obj)

    context = {
        'title' : 'Exams | '+ obj.name,
        'obj':obj,
        'days':obj.get_left_days(),
        'students': students,
        'youtube_obj':youtube_obj
    }
    
    if 'subscribe' in request.POST:
        obj.student.add(request.user)
        messages.success(request,f'Subscribed to {obj.name} exam.')
        return redirect('view_exam',obj.id)
    
    if 'unsubscribe' in request.POST:
        obj.student.remove(request.user)
        messages.success(request,f'Unsubscribed to {obj.name} exam.')
        return redirect('view_exam',obj.id)

    return render(request,'mainapp/view_exam.html',context)

def view_institute(request,id):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    obj = Institute.objects.get(id=id)
    exam_obj = Exam.objects.all()
    for o in exam_obj:
        if o.institute != obj:
            exam_obj = exam_obj.exclude(id=o.id)
    '''
    exam_obj = exam_obj.group_by('institute')
    exam_obj =  exam_obj.prefetch_related('institute').filter(institute__id=id)
    print(exam_obj)'''

    context = {
        'title' : 'Institute | '+ obj.name,
        'obj':obj,
        'exam_obj':exam_obj
    }
    if 'subscribe' in request.POST:
        obj.student.add(request.user)
        messages.success(request,f'Subscribed to {obj.name} exam.')
        return redirect('view_institute',obj.id)
    
    if 'unsubscribe' in request.POST:
        obj.student.remove(request.user)
        messages.success(request,f'Unsubscribed to {obj.name} exam.')
        return redirect('view_institute',obj.id)

    return render(request,'mainapp/view_institute.html',context)

def institutes(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    obj = Institute.objects.all()

    context = {
        'title' : 'Institutes',
        'i_obj': obj
    }

    return render(request,'mainapp/institutes.html',context)

def download_pdf(request,id,type):
    obj = Exam.objects.get(id=id)
    # type1 = rules type2 = marks typ3=syllabus
    if type == 1:
        try:
            pdf = obj.rules_pdf
            response = HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment'
            return response
        except:
            return redirect('errorpage')
    if type == 2:
        try:
            pdf = obj.syllabus_pdf
            response = HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment'

            return response
        except:
            return redirect('errorpage')
    if type == 3:
        try:
            pdf = obj.marking_scheme
            response = HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment'

            return response
        except:
            return redirect('errorpage')

def generate_rules(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    if request.method == 'POST':
        imp = request.POST.get("important")
        try:
            others = request.POST.get("others")
        except:
            pass
        return redirect('generate_rules_pdf',imp=imp,others=others)

    return render(request,'mainapp/generate_rules.html')


def generate_rules_pdf(request,imp,others):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    template = loader.get_template('mainapp/generate_rules_pdf.html')
    html = template.render({'imp':imp,'others':others})
    options = {
        'page-size':'Letter',
        'encoding':"UTF-8",
    }
    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'

    return response

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('errorpage')

    logout(request)
    return redirect('signin') 

def notifyuser(request):
    pass

def send_mail_on_update():
    pass



    