function createBookElement(book, target_id) {
    const bookElement = document.createElement('div');
    bookElement.classList.add('card-sm', 'mb-4');
    const title = document.createElement('div');
    title.textContent = book.title;
    bookElement.appendChild(title);

    // マージボタン
    const mergeBtn = document.createElement('a');
    mergeBtn.textContent = 'マージ';
    mergeBtn.classList.add('btn', 'btn-primary');
    mergeBtn.href = `/manage/books/${target_id}/merge/${book.id}/`;
    bookElement.appendChild(mergeBtn);

    return bookElement;
}

document.addEventListener('DOMContentLoaded', function() {
    // 検索APIを使って検索する
    const searchBtn = document.getElementById('search-btn');
    const bookList = document.getElementById('book-list');
    const bookId = searchBtn.dataset.bookId;
    
    searchBtn.addEventListener('click', function() {
        const query = document.getElementById('query');
        const url = searchBtn.dataset.url;
        const token = getCsrfToken();
        console.log(bookId)


        if (!query) {
            return;
        }

        fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                query: query.value,
                page: 1
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            }
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                console.log('error');
            }
        }).then(books => {
            // bookListの全ての子要素を消す
            while (bookList.firstChild) {
                bookList.removeChild(bookList.firstChild);
            }

            books.forEach(book => {
                const bookElement = createBookElement(book, bookId);
                console.log(bookElement);
                bookList.appendChild(bookElement);
            })
        })
    });
});