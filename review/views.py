# TODO
from review.application.usecases import ReviewUsecase


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# API
@csrf_exempt
@login_required
def create_review(request, book_id):
    if request.method != "POST":
        return JsonResponse({"error": "Postのみ受け付けています。"}, status=400)

    usecase = ReviewUsecase(request.user, book_id, request.POST)

    response, status = usecase.execute()

    return JsonResponse(response, status=status)
