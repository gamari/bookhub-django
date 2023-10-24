async function createMemo(url, body_data, csrf_token) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: body_data
    });
    
    const data = await response.json();

    if (data.result === 'success') {
        return data;
    } else {
        alert("メモ作成に失敗しました。");
        throw new Error("メモ作成に失敗しました。");
    }
}


function initialize() {
    const memoList = document.querySelector("#memoList");
    const memoForm = document.querySelector("#memoForm");
    const createMemoButton = document.querySelector("#createMemoButton");
    const memoContent = document.querySelector("#id_content");
    const noMemoTitle = document.querySelector("#no-memo-title");

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
            memoList.prepend(createMemoElement(data));
            memoContent.value = '';
            if (noMemoTitle) noMemoTitle.remove();
        } catch (error) {
            console.error("Error creating memo:", error);
        }
    });
}

document.addEventListener('DOMContentLoaded', initialize);