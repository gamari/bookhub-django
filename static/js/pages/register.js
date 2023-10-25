document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("google-auth-link").addEventListener("click", function(event) {
        var termsChecked = document.getElementById("id_terms_agreed").checked;
    
        if (!termsChecked) {
            event.preventDefault();
            alert("利用規約に同意してください。");
        }
    });
});