// TODO 移動させる
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createMemoElement(data) {
    let memoList = document.querySelector("#memoList");
    let newMemo = document.createElement('li');
    newMemo.classList.add('memo-item');
    newMemo.innerHTML = `<p>${data.created_at}</p><p>${data.content}</p>`;
    memoList.prepend(newMemo);

    // TODO 削除ボタンの追加
    // TODO リスナーを追加する
    let deleteButton = document.createElement('button');
    deleteButton.classList.add('memo-item-delete-button');
    deleteButton.dataset.memoId = data.id;
    deleteButton.dataset.action = data.delete_url;
    let deleteIcon = document.createElement('i');
    deleteIcon.classList.add('fa-regular', 'fa-trash-can');
    deleteIcon.style.color = '#160160160';
    deleteButton.appendChild(deleteIcon);
    newMemo.appendChild(deleteButton);


    // TODO フォームの中身を削除
    let memoContent = document.querySelector("#id_content");
    memoContent.value = '';

    let noMemoTitle = document.querySelector("#no-memo-title");
    if (noMemoTitle) {
        noMemoTitle.remove();
    }
}


// リスナー設定
document.addEventListener('DOMContentLoaded', function () {
    // メモフォームを設定
    let memoForm = document.querySelector("#memoForm");
    let createMemoButton = document.querySelector("#createMemoButton");

    createMemoButton.addEventListener("click", function (event) {
        event.preventDefault();
        let formData = new FormData(memoForm);

        if (formData.get('content') === '') {
            alert("メモの内容を入力してください。");
            return;
        }

        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }

        let postUrl = memoForm.dataset.action;

        createMemo(
            postUrl,
            formData,
            document.querySelector("[name=csrfmiddlewaretoken]").value
        ).then(data => {
            createMemoElement(data);
        });
    });


    // 削除ボタンのイベントリスナーを登録
    document.querySelectorAll('.memo-item-delete-button').forEach(function (button) {
        button.addEventListener('click', function () {
            const isOk = confirm('メモを削除しますか？');

            if (!isOk) return;

            const memoId = this.dataset.memoId;
            const actionUrl = this.dataset.action;

            deleteMemo(memoId, actionUrl).then(data => {
                button.closest('.memo-item').remove();
            });
        });
    });
});