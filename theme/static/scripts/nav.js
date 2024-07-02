document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleBtn');
    const nav = document.querySelector('.myNav');

    toggleBtn.addEventListener('click', function () {
        nav.classList.toggle('max-md:hidden');
    });
});