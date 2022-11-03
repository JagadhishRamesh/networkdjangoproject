from django.urls import path
from . import views
from .views import compliancehome

urlpatterns = [
    path('', views.compliancehome , name='compliance-check-homepage'),
    path('summary/', views.compliancesummary, name='compliance-check-summary'),
    path('logs/', views.compliancelogs, name='compliance-check-logs'),
    path('status/', views.compliancestatus, name='compliance-status')
]