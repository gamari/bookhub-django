document.addEventListener("DOMContentLoaded", function () {
    let memoForm = document.querySelector("#memoForm");
    let createMemoButton = document.querySelector("#createMemoButton");

    createMemoButton.addEventListener("click", function (event) {
        console.log("click")
        event.preventDefault();
        let formData = new FormData(memoForm);

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
                    newMemo.innerHTML = `<p>${data.created_at}</p><p>${data.content}</p>`;
                    memoList.prepend(newMemo);
                } else {
                    alert("エラーが発生しました。");
                }
            });
    });
});