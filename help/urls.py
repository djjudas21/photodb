from django.urls import path
from django.views.generic import TemplateView
from help.views import ConditionListView

app_name = 'help'
urlpatterns = [

    # Static pages
    path('', TemplateView.as_view(template_name='index.html'), name='help'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('faq', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('condition', ConditionListView.as_view(), name='condition-list'),
    path('api', TemplateView.as_view(template_name='api.html'), name='api'),
]
