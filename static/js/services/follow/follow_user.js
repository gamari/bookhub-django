document.addEventListener("DOMContentLoaded", function () {
    const followButtons = document.querySelectorAll("[data-follow-button]");
    const followersCountElem = document.querySelector("#followers-count");

    followButtons.forEach(button => {
        button.addEventListener("click", function () {
            handleFollowButtonClick(this, followersCountElem);
        });
    });
});

function handleFollowButtonClick(button, followersCountElem) {
    const targetId = button.getAttribute("data-target-id");
    const isCurrentlyFollowing = button.getAttribute("data-is-follow") === "True";
    const csrfToken = getCookie('csrfmiddlewaretoken');
    const apiUrl = getApiUrl(targetId, isCurrentlyFollowing);

    toggleFollow(apiUrl, csrfToken)
        .then(isFollowed => {
            updateButtonState(button, isFollowed);
            updateFollowerCount(followersCountElem, isFollowed);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function getApiUrl(targetId, isFollow) {
    return isFollow ? `/api/unfollow/${targetId}/` : `/api/follow/${targetId}/`;
}

function toggleFollow(apiUrl, csrfToken) {
    return fetch(apiUrl, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken
        },
    })
    .then(response => response.json())
    .then(data => data.followed);
}

function updateButtonState(button, isFollowed) {
    if (isFollowed) {
        button.textContent = "フォロー解除";
        button.classList.remove("btn-primary");
        button.setAttribute("data-is-follow", "True");
    } else {
        button.textContent = "フォローする";
        button.classList.add("btn-primary");
        button.setAttribute("data-is-follow", "False");
    }
}

function updateFollowerCount(followersCountElem, isFollowed) {
    const currentCount = Number(followersCountElem.textContent);
    followersCountElem.textContent = isFollowed ? currentCount + 1 : currentCount - 1;
}
