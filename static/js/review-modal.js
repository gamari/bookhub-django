document.addEventListener("DOMContentLoaded", function () {
    const reviewModal = document.getElementById('reviewModal');
    const openReviewModalButton = document.getElementById('openReviewModalButton');
    const closeReviewModalButton = document.getElementById('closeReviewModalButton');
    const reviewSubmitButton = document.getElementById('review-submit');
    const reviewForm = document.getElementById('reviewForm');

    const deleteReviewButton = document.querySelector('#delete-review');

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function openModal() {
        reviewModal.style.display = 'block';
    }

    function closeModal() {
        reviewModal.style.display = 'none';
    }

    function submitReview() {
        const formData = new FormData(reviewForm);
        const reviewUrl = reviewForm.getAttribute('action');

        fetch(reviewUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error submitting review:', error)
        });
    }

    function deleteReview() {
        const deleteUrl = deleteReviewButton.getAttribute('data-url');
        console.log(deleteUrl); 

        fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => {
            if (response.status === 204) {
                location.reload()
            } else {
                console.error('削除に失敗しました。');
            }
        })
        .catch(error => {
            console.error('削除に失敗しました。', error)
        });
    }

    if (openReviewModalButton) openReviewModalButton.addEventListener('click', openModal);
    if (closeReviewModalButton) closeReviewModalButton.addEventListener('click', closeModal);
    if (reviewSubmitButton) reviewSubmitButton.addEventListener('click', submitReview);

    // 削除ボタンの処理
    if (deleteReviewButton) deleteReviewButton.addEventListener("click", deleteReview);
});
