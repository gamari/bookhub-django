from django.shortcuts import render

from contact.forms import ContactForm


def contact_page(request):
    form = ContactForm(request.POST or None)

    message = None

    if form.is_valid():
        form.save()
        form = ContactForm()
        message = "送信しました"

    return render(request, "contact.html", {"form": form, "message": message})
