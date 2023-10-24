from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def management_dashboard(request):
    context = {}
    return render(request, "pages/manage-dashboard.html", context)
