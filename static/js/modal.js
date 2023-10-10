// TODO 削除予定
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('openModalButton').addEventListener('click', function () {
        console.log('openModalButton');
        document.getElementById('reviewModal').style.display = 'block';
    });

    document.getElementById('closeModalButton').addEventListener('click', function () {
        document.getElementById('reviewModal').style.display = 'none';
    });

    document.getElementById('footerCloseModalButton').addEventListener('click', function () {
        document.getElementById('reviewModal').style.display = 'none';
    });
});


