from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import BookSelection, BookSelectionLike

# TODO CSRFの検討を行う
@csrf_exempt
def like_book_selection(request, selection_id):
    if request.method == "POST":
        user = request.user
        print(selection_id)
        selection = get_object_or_404(BookSelection, id=selection_id)

        existing_like = BookSelectionLike.objects.filter(user=user, selection=selection).first()

        if existing_like:
            existing_like.delete()
            action = "unliked"
        else:
            BookSelectionLike.objects.create(user=user, selection=selection)
            action = "liked"

        return JsonResponse({'action': action})

    return HttpResponseBadRequest("メソッドが間違っています。")
