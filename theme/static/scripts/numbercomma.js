let change = document.querySelectorAll('.font-bold');

for (let i = 0; i < change.length; i++) {
    change[i].textContent = change[i].textContent.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


