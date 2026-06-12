from django.shortcuts import render
from milestone1.abha_login.views.dashboard_views import profile_dashboard

def profile_dashboard(request):
    return render(request, 'dashboard.html')