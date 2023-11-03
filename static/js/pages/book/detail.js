/*
書籍詳細画面のJavaScript。
*/

/** リスナー */
function deleteListener(button) {
    const isOk = confirm('削除してもよろしいですか？');

    if (!isOk) return;

    const memoId = button.dataset.memoId;
    const actionUrl = button.dataset.action;

    deleteMemo(memoId, actionUrl).then(data => {
        button.closest('.memo-item').remove();
    });
}


/** トグルボタンの初期設定。 */
function initializeToggles() {
    const btnReviews = document.getElementById('btn-reviews');
    const btnTimeline = document.getElementById('btn-timeline');
    const btnBookDetail = document.getElementById('btn-book-detail');
    
    const sectionReviews = document.getElementById('reviews-section');
    const sectionTimeline = document.getElementById('timeline-section');
    const sectionBookDetail = document.getElementById('book-detail-section');
    
    function showTimeline() {
        reset();
        sectionTimeline.style.display = 'block';
        btnTimeline.classList.add('badge-info');
    }

    function showReviews() {
        reset();
        sectionReviews.style.display = 'block';
        btnReviews.classList.add('badge-info');
    }

    function showBookDetail() {
        reset();
        sectionBookDetail.style.display = 'block';
        btnBookDetail.classList.add('badge-info');
    }

    btnReviews.addEventListener('click', showReviews);
    btnTimeline.addEventListener('click', showTimeline);
    btnBookDetail.addEventListener('click', showBookDetail);

    function reset() {
        sectionReviews.style.display = 'none';
        sectionTimeline.style.display = 'none';
        sectionBookDetail.style.display = 'none';
        btnReviews.classList.remove('badge-info');
        btnTimeline.classList.remove('badge-info');
        btnBookDetail.classList.remove('badge-info');
    }

    // 初期化
    showTimeline();
}

function initializeGetMemoList() {
    const btnGetMemoList = document.getElementById('get-memo-list-btn');
    const bookId = document.getElementById('book-id').value;
    const memoList = document.getElementById('memo-list');
    let timelinePage = 1;

    btnGetMemoList.addEventListener('click', function() {
        timelinePage++;
        const url = `/api/books/${bookId}/memos/?page=${timelinePage}`;
        fetch(url)
            .then(response => response.json())
            .then(memos => {
                memos.forEach(memo => {
                    const newMemo = createMemoElement(memo, false);
                    memoList.appendChild(newMemo);
                })
            });
    });
}

function initializeCreateMemo() {
    const memoList = document.querySelector("#memo-list");
    const memoForm = document.querySelector("#memo-form");
    const createMemoButton = document.querySelector("#create-memo-button");
    const memoContent = document.querySelector("#id_content");
    const noMemoTitle = document.querySelector("#no-memo-title");

    // 投稿フォームの設定
    createMemoButton.addEventListener("click", async function (event) {
        event.preventDefault();
        const formData = new FormData(memoForm);

        if (formData.get('content') === '') {
            alert("メモの内容を入力してください。");
            return;
        }

        const postUrl = memoForm.dataset.action;

        try {
            const data = await createMemo(postUrl, formData, getCookie('csrfmiddlewaretoken'));

            if (noMemoTitle) noMemoTitle.remove();

            const newMemo = createMemoElement(data)
            memoList.prepend(newMemo);
            memoContent.value = '';
        } catch (error) {
            console.error( error);
        }
    });

    // 削除ボタンの設定
    const deleteButtonList = document.querySelectorAll('.memo-item__delete');
    deleteButtonList.forEach(function (button) {
        button.addEventListener('click', function (event) {
            deleteListener(button);
        });
    });
}


document.addEventListener('DOMContentLoaded', function() {
    initializeToggles();
    initializeGetMemoList();
    initializeCreateMemo();
});