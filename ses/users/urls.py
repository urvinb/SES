from django.urls import path


from . import views

urlpatterns = [
    path('', views.common, name='common'),
    path('student/', views.signin, name='signin'),
    path('student/register/<int:id>/<int:tab>', views.register, name='register_s'),
    path('error', views.errorpage, name='errorpage')
]