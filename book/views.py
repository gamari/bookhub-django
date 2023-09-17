from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def show_dashboard(request):
    print(request.user)
    return render(request, "dashboard.html")