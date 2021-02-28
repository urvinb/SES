from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_rules', views.generate_rules, name='generate_rules'),
    path('generate_rules_pdf/<str:imp>/<str:others>', views.generate_rules_pdf, name='generate_rules_pdf'),
    path('subscribed', views.subscriptions, name='subscriptions'),
    path('institutes', views.institutes, name='institutes'),
    path('domains/<int:id>', views.domains, name='domains'),
    path('view_exam/<int:id>', views.view_exam, name='view_exam'),
    path('view_institute/<int:id>', views.view_institute, name='view_institute'),
    path('download_pdf/<int:id>/<int:type>', views.download_pdf, name='download_pdf'),
    path('logout', views.logout_view, name='main_logout'),
]