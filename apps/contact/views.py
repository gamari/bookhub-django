from django.shortcuts import render

from apps.contact.forms import ContactForm


def contact_page(request):
    form = ContactForm(request.POST or None)

    message = None

    if form.is_valid():
        form.save()
        form = ContactForm()
        message = "送信しました"

    return render(request, "contact.html", {"form": form, "message": message})

def help_activity_page(request):
    return render(request, "pages/help_activity.html")

# 利用規約ページ
def terms_page(request):
    return render(request, "pages/terms.html")

def privacy_page(request):
    return render(request, "pages/privacy.html")