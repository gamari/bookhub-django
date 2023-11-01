from django.shortcuts import render

def recommend_book(request, book_id):
    # TODO レコメンドを作る
    # TODO manageに入れる

    return render(request, 'ads/recommend_book.html')