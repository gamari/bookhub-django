# TODO
from django.shortcuts import get_object_or_404, render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.review.application.usecases import ReviewUsecase
from apps.review.models import Review

Account = get_user_model()


def user_reviews(request, user_id):
    account = get_object_or_404(Account, pk=user_id)
    reviews = Review.objects.filter(user=account)
    rating_range = range(1, 6)
    return render(
        request,
        "account_reviews.html",
        {"account": account, "reviews": reviews, "rating_range": rating_range},
    )


# API
@csrf_exempt
@login_required
def create_review(request, book_id):
    if request.method != "POST":
        return JsonResponse({"error": "Postのみ受け付けています。"}, status=400)

    usecase = ReviewUsecase(request.user, book_id, request.POST)

    response, status = usecase.execute()

    return JsonResponse(response, status=status)
