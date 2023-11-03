// リスナー
function deleteListener(button) {
    const isOk = confirm('削除してもよろしいですか？');

    if (!isOk) return;

    const memoId = button.dataset.memoId;
    const actionUrl = button.dataset.action;

    deleteMemo(memoId, actionUrl).then(data => {
        button.closest('.memo-item').remove();
    });
}

document.addEventListener("DOMContentLoaded", function () {
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
});