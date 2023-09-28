document.addEventListener("DOMContentLoaded", function () {
    // TODO openReviewModalはない場合が存在するのでそれを修正する
    // レビューモーダルの処理を実装
    document.getElementById('openReviewModalButton').addEventListener('click', function () {
        document.getElementById('reviewModal').style.display = 'block';
    });

    document.getElementById('closeReviewModalButton').addEventListener('click', function () {
        document.getElementById('reviewModal').style.display = 'none';
    });

    document.getElementById('review-submit').addEventListener('click', function () {
        // レビュー処理
        const reviewForm = document.getElementById('reviewForm');
        const formData = new FormData(reviewForm);
        const reviewUrl = reviewForm.getAttribute('action');

        fetch(reviewUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    // handle error (show message to user or something)
                } else {
                    // 画面をリロードする
                    location.reload();
                }
            })
            .catch(error => console.error('Error submitting review:', error));

    });

});


