document.addEventListener("DOMContentLoaded", function() {
    const bookSelections = document.querySelectorAll(".book-selection");

    bookSelections.forEach((book) => {
        book.addEventListener("click", function() {
            const checkbox = this.querySelector("input[type=checkbox]");
            checkbox.checked = !checkbox.checked;

            if (checkbox.checked) {
                this.classList.add("selected");
                this.classList.add("selection-selected")
            } else {
                this.classList.remove("selected");
                this.classList.remove("selection-selected")
            }
        });
    });
});