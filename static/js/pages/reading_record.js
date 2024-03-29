// リスナー
function deleteListener(button) {
    const isOk = confirm('削除してもよろしいですか？');

    if (!isOk) return;

    const memoId = button.dataset.memoId;
    const actionUrl = button.dataset.action;

    deleteMemo(memoId, actionUrl).then(data => {
        button.closest('.memo-item').remove();
    })
    .catch(error => {
        alert("削除に失敗しました。")
    });;
}

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

function initializeForm() {
    const createMemoButton = document.querySelector("#create-memo-button");
    const memoContent = document.querySelector("#memo-content");

    // 投稿フォームの設定
    createMemoButton.addEventListener("click", async function (event) {
        event.preventDefault();
        postMemo();
    });

    memoContent.addEventListener('keydown', async function (event) {
        if (event.ctrlKey && event.key === 'Enter') {
            event.preventDefault();
            postMemo();
        }
    });
}

function initializeDeleteButtons() {
    // 削除ボタンの設定
    const deleteButtonList = document.querySelectorAll('.memo-item__delete');
    deleteButtonList.forEach(function (button) {
        button.addEventListener('click', function (event) {
            deleteListener(button);
        });
    });
}

function initializeGetButton() {
    const getMemoListButton = document.querySelector('#get-memo-list-btn');
    const memoList = document.querySelector('#memo-list');
    const loading = document.querySelector('.loading');
    const book_id = document.querySelector('#book_id').value;
    let oldestDate;

    if (memoList.lastElementChild) {
        oldestDate = memoList.lastElementChild.dataset.date
    }

    getMemoListButton.addEventListener('click', function() {
        getMyselfMemoListByBookAndDate(book_id, oldestDate).then(json => {
            getMemoListButton.style.display = 'block';

            if (json.length === 0) {
                getMemoListButton.style.display = 'none';
                return;
            }
    
            json.forEach(data => {
                memoList.appendChild(createMemoElement(data));
            })

            const created_at  = json[json.length - 1]['created_at']
            if (created_at) {
                oldestDate = created_at
            }
        })
    });
}

document.addEventListener("DOMContentLoaded", function () {
    initializeForm();
    initializeDeleteButtons();
    initializeGetButton();
});

