 const closeButton = document.getElementById('closePopup');
 const popup = document.getElementById('popup');
 const openButton = document.getElementById('openPopup');

 const closeButton2 = document.getElementById('closePopup2');
 const popup2 = document.getElementById('popup2');
 const openButton2 = document.getElementById('openPopup2');

 openButton.addEventListener('click', () => {
   popup.classList.remove('hidden');
 });

 openButton2.addEventListener('click', () => {
  popup2.classList.remove('hidden');
});


 closeButton.addEventListener('click', () => {
   popup.classList.add('hidden');
 });

 closeButton2.addEventListener('click', () => {
  popup2.classList.add('hidden');
});

