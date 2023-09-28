document.addEventListener("DOMContentLoaded", function () {
    let memoForm = document.querySelector("#memoForm");
    let createMemoButton = document.querySelector("#createMemoButton");

    createMemoButton.addEventListener("click", function (event) {
        event.preventDefault();
        let formData = new FormData(memoForm);

        if (formData.get('content') === '') {
            alert("メモの内容を入力してください。");
            return;
        }

        // フォームデータの中身を確認
        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }

        let postUrl = memoForm.dataset.action;
        fetch(postUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.result === 'success') {
                    let memoList = document.querySelector("#memoList");
                    let newMemo = document.createElement('li');
                    newMemo.classList.add('memo-item');
                    newMemo.innerHTML = `<p>${data.created_at}</p><p>${data.content}</p>`;
                    memoList.prepend(newMemo);
                    

                    // TODO フォームの中身を削除
                    let memoContent = document.querySelector("#memoContent");
                    memoContent.value = '';

                    let noMemoTitle = document.querySelector("#no-memo-title");
                    if (noMemoTitle) {
                        noMemoTitle.remove();
                    }
                } else {
                    alert("エラーが発生しました。");
                }
            });
    });
});