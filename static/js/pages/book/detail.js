function initializeToggles() {
    const btnReviews = document.getElementById('btn-reviews');
    const btnTimeline = document.getElementById('btn-timeline');
    const btnBookDetail = document.getElementById('btn-book-detail');
    
    const sectionReviews = document.getElementById('reviews-section');
    const sectionTimeline = document.getElementById('timeline-section');
    const sectionBookDetail = document.getElementById('book-detail-section');

    btnReviews.addEventListener('click', function () {
        reset();
        sectionReviews.style.display = 'block';
        btnReviews.classList.add('badge-info');
    });

    btnTimeline.addEventListener('click', function () {
        reset();
        sectionTimeline.style.display = 'block';
        btnTimeline.classList.add('badge-info');
    });

    btnBookDetail.addEventListener('click', function () {
        reset();
        sectionBookDetail.style.display = 'block';
        btnBookDetail.classList.add('badge-info');
    });

    function reset() {
        sectionReviews.style.display = 'none';
        sectionTimeline.style.display = 'none';
        sectionBookDetail.style.display = 'none';
        btnReviews.classList.remove('badge-info');
        btnTimeline.classList.remove('badge-info');
        btnBookDetail.classList.remove('badge-info');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initializeToggles();

    // TODO メモの取得処理などを実装する
    const btnGetMemoList = document.getElementById('get-memo-list-btn');
    const bookId = document.getElementById('book-id').value;
    const memoList = document.getElementById('memo-list');
    let timelinePage = 1;

    btnGetMemoList.addEventListener('click', function() {
        timelinePage++;
        const url = `/api/books/${bookId}/memos/?page=${timelinePage}`;
        console.log(url);
        fetch(url)
            .then(response => response.json())
            .then(memos => {
                console.log(memos)
                memos.forEach(memo => {
                    const newMemo = createMemoElement(memo, false);
                    memoList.appendChild(newMemo);
                })
            });
    });
});