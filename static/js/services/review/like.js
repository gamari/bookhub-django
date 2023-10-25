document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll(".like-btn");
    
    likeButtons.forEach(likeButton => {
        likeButton.addEventListener("click", async function () {
            const isLiked = likeButton.dataset.liked === "true";
            const reviewId = likeButton.dataset.selectionId;
            const likeIcon = likeButton.querySelector(".like-icon");
            const likeCountElem = likeButton.querySelector(".like-count");
    
            const url = `/api/review/${reviewId}/${isLiked ? "unlike" : "like"}/`;
            let csrfToken = getCsrfToken();
    
            try {
                const response = await fetch(url, {
                    method: isLiked ? "DELETE" : "POST",
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                });
    
                if (response.ok) {
                    likeButton.dataset.liked = !isLiked;
                    likeButton.style.color = !isLiked ? "#FF0000" : "#666";

                    if (isLiked) {
                        likeCountElem.textContent = parseInt(likeCountElem.textContent) - 1;
                    } else {
                        likeCountElem.textContent = parseInt(likeCountElem.textContent) + 1;
                    }
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail);
                }
    
            } catch (error) {
                console.error("Error liking/unliking: ", error);
            }
        })
    });
});
