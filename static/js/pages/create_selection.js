document.addEventListener("DOMContentLoaded", function() {
    const bookSelections = document.querySelectorAll(".book-selection");
    const selectedCountElem = document.getElementById("selected-count");

    function updateSelectedCount() {
        const checkedBooks = document.querySelectorAll(".book-selection.selected").length;
        if (checkedBooks > 0) {
            selectedCountElem.textContent = ` (${checkedBooks}件の選択)`;
        } else {
            selectedCountElem.textContent = "";
        }
    }

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

            updateSelectedCount();
        });
    });
});