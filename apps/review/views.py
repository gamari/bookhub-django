from django.shortcuts import get_object_or_404, render

from django.contrib.auth import get_user_model

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

