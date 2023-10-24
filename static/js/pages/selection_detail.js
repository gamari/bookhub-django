// like.js

document.addEventListener('DOMContentLoaded', function() {
    const likeIcon = document.getElementById('like-icon');
    if (likeIcon) {

        likeIcon.addEventListener('click', function() {
            const isLiked = likeIcon.getAttribute('data-liked') === "true";
            const likeBtn = document.getElementById('like-btn');
            const selectionId = likeIcon.getAttribute('data-selection-id');
            const likeCount = document.getElementById('like-count');
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                
            fetch(`/api/selection/${selectionId}/like/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.action === 'liked') {
                    likeBtn.style.color = '#FF0000';
                    likeIcon.setAttribute('data-liked', 'true');
                    likeCount.textContent = Number(likeCount.textContent) + 1;
                } else {
                    likeBtn.style.color = '#666';
                    likeIcon.setAttribute('data-liked', 'false');
                    likeCount.textContent = Number(likeCount.textContent) - 1;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
