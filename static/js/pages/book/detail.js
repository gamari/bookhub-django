/*
書籍詳細画面のJavaScript。
*/
async function postMemo() {
    const memoList = document.querySelector("#memo-list");
    const memoForm = document.querySelector("#memo-form");
    const memoContent = document.querySelector("#memo-content");
    const noMemoTitle = document.querySelector("#no-memo-title");

    const formData = new FormData(memoForm);

    if (formData.get('content') === '') {
        alert("メモの内容を入力してください。");
        return;
    }

    // TODO URLは渡したくない
    const postUrl = memoForm.dataset.action;

    try {
        const data = await createMemo(postUrl, formData);

        if (noMemoTitle) noMemoTitle.remove();

        const newMemo = createMemoElement(data)
        memoList.prepend(newMemo);
        memoContent.value = '';
    } catch (error) {
        const message = error.message;
        if (message) {
            alert(message);
        }
        console.error(error);
    }
}

// TODO ランク作成は関数化するべき
async function getRanking() {
    const bookId = document.getElementById('book_id').value;
    const apiUrl = `/api/ranking/books/${bookId}/memos/users/`;

    // TODO 関数にする
    const response = await fetch(apiUrl);
    const data = await response.json();
    const rankingList = document.getElementById('ranking-list');
    rankingList.innerHTML = '';

    if (data.length === 0) {
        const noRanking = document.createElement('div');
        noRanking.innerText = '参加者がいません';
        rankingList.appendChild(noRanking);
        return;
    }

    // TODO まだ無ければ、ランキングがありません。と表示する
    data
    .sort((a, b) => {
        return b.memos_count - a.memos_count > 0 ? 1 : -1;
    })
    .forEach((user, index) => {
        const rankItem = document.createElement('div');
        rankItem.classList.add('user-info');

        // rankItemを分解して作る
        const rankHeader = document.createElement('div');
        rankHeader.classList.add('text-primary');
        rankHeader.innerText = `${index + 1}位`;

        const rankBody = document.createElement('div');
        rankBody.classList.add('user-info__body');
        rankBody.classList.add('row-center');
        rankBody.classList.add('gap-4');

        const userLink = document.createElement('a');
        userLink.classList.add('user-icon-sm');
        userLink.classList.add('user-icon');
        userLink.href = `/user/${user.username}/`;

        const rankImage = document.createElement('div');
        if (user.profile_image) {
            rankImage.innerHTML = `<img src="${user.profile_image}" class="user-icon user-icon-sm" />`;
        } else {
            rankImage.innerHTML = `<i class="fa-regular fa-face-smile fa-xl" style="color: #888"></i>`;
        }

        userLink.appendChild(rankImage);

        const rankUsername = document.createElement('div');
        rankUsername.innerText = user.username;

        rankBody.appendChild(userLink);
        rankBody.appendChild(rankUsername);

        rankItem.appendChild(rankHeader);
        rankItem.appendChild(rankBody);

        rankingList.appendChild(rankItem);
    });
}


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
    const getMemoListButton = document.querySelector('#get-memo-list-btn');
    const memoList = document.querySelector('#memo-list');
    const loading = document.querySelector('.loading');
    const book_id = document.querySelector('#book_id').value;
    let oldestDate;

    if (memoList.lastElementChild) {
        oldestDate = memoList.lastElementChild.dataset.date
    }

    getMemoListButton.addEventListener('click', function () {
        getMemoListByBookAndDate(book_id, oldestDate).then(json => {
            getMemoListButton.style.display = 'block';

            if (json.length === 0) {
                getMemoListButton.style.display = 'none';
                return;
            }

            json.forEach(data => {
                memoList.appendChild(createMemoElement(data));
            })

            const created_at = json[json.length - 1]['created_at']
            if (created_at) {
                oldestDate = created_at
            }
        })
    });
}

function initializeCreateMemo() {
    const createMemoButton = document.querySelector("#create-memo-button");
    const memoContent = document.querySelector("#memo-content");

    // 投稿フォームの設定
    createMemoButton.addEventListener("click", async function (event) {
        event.preventDefault();
        postMemo();
    });

    // 削除ボタンの設定
    const deleteButtonList = document.querySelectorAll('.memo-item__delete');
    deleteButtonList.forEach(function (button) {
        button.addEventListener('click', function (event) {
            deleteListener(button);
        });
    });

    memoContent.addEventListener('keydown', async function (event) {
        if (event.ctrlKey && event.key === 'Enter') {
            event.preventDefault();
            postMemo();
        }
    });
}

async function initializeRanking() {
    getRanking();
}


document.addEventListener('DOMContentLoaded', function () {
    initializeToggles();
    initializeGetMemoList();
    initializeCreateMemo();
    initializeRanking();
});