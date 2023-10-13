// TODO followカウントを変更する
document.addEventListener("DOMContentLoaded", function () {
    const followButtons = document.querySelectorAll("[data-follow-button]");

    followButtons.forEach(button => {
        button.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target-id");
            const isFollow = this.getAttribute("data-is-follow") === "True";
            const apiUrl = isFollow
                ? `/api/unfollow/${targetId}/`
                : `/api/follow/${targetId}/`;
            const csrfToken = this.getAttribute("data-csrf-token");

            // TODO csrfTokenが取得できていない
            // console.log(csrfToken);

            fetch(apiUrl, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.followed) {
                    this.textContent = "フォロー解除";
                    this.classList.remove("btn-primary");
                    this.setAttribute("data-is-follow", "True");
                } else {
                    this.textContent = "フォロー";
                    this.classList.add("btn-primary");
                    this.setAttribute("data-is-follow", "False");
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    });
});
