from apps.management.forms import TweetForm, TweetTagForm
from apps.management.models import Tweet, TweetTag


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render


@user_passes_test(lambda u: u.is_superuser)
def management_tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")

    context = {
        "tweets": tweets,
    }

    return render(request, "pages/manage/tweet/list.html", context)


@user_passes_test(lambda u: u.is_superuser)
def management_tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management_tweet_list')
    else:
        form = TweetForm()
    context = {
        "form": form,
    }

    return render(request, "pages/manage/tweet/create.html", context)


@user_passes_test(lambda u: u.is_superuser)
def management_tweet_edit(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    if request.method == "POST":
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('management_tweet_list')
    else:
        form = TweetForm(instance=tweet)

    context = {
        "tweet": tweet,
        "form": form,
    }
    return render(request, "pages/manage/tweet/edit.html", context)

# タグ
@user_passes_test(lambda u: u.is_superuser)
def management_tweet_tag_list(request):
    tags = TweetTag.objects.all()
    
    context = {
        "tags": tags,
    }
    
    return render(request, "pages/manage/tweet/tag-list.html", context)

@user_passes_test(lambda u: u.is_superuser)
def management_create_tweet_tag(request):
    if request.method == "POST":
        form = TweetTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management_tweet_tag_list')
    else:
        form = TweetTagForm()
        
    context = {
        "form": form,
    }

    return render(request, "pages/manage/tweet/tag-create.html", context)