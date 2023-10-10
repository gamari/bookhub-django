// TODO pages/reading_recordに移す
// TODO 処理をリファクタリングする
document.addEventListener("DOMContentLoaded", function () {
    const openReviewModalButton = document.getElementById('openReviewModalButton');
    const closeReviewModalButton = document.getElementById('closeReviewModalButton');
    const reviewSubmitButton = document.getElementById('review-submit');

    if (openReviewModalButton) {
        openReviewModalButton.addEventListener('click', function () {
            document.getElementById('reviewModal').style.display = 'block';
        });
    }

    if (closeReviewModalButton) {
        closeReviewModalButton.addEventListener('click', function () {
            document.getElementById('reviewModal').style.display = 'none';
        });
    }

    if (reviewSubmitButton) {
        reviewSubmitButton.addEventListener('click', function () {
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
    }
});


