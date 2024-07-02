const searchInput = document.getElementById('searchGuarantor');
const searchResults = document.getElementById('guarantorResults');
const selectedUserIdInput = document.getElementById('selectedUserId');

const users = [
  { id: 1, name: 'User 1' },
  { id: 2, name: 'User 2' },
  { id: 3, name: 'User 3' },
  { id: 4, name: 'User 4' }
];

searchInput.addEventListener('input', function () {
  const query = this.value.trim();
  if (query.length === 0) {
    searchResults.innerHTML = '';
    searchResults.classList.add('hidden');
    return;
  }

  const filteredUsers = users.filter(user => user.name.toLowerCase().includes(query.toLowerCase()));

  searchResults.innerHTML = '';
  if (filteredUsers.length > 0) {
    filteredUsers.forEach(user => {
      const resultElement = document.createElement('div');
      resultElement.classList.add('cursor-pointer', 'p-2', 'hover:bg-gray-800');;
      resultElement.textContent = user.name;
      resultElement.addEventListener('click', function () {
        searchInput.value = user.name;
        selectedUserIdInput.value = user.id;
        searchResults.innerHTML = '';
        searchResults.classList.add('hidden');
      });
      searchResults.appendChild(resultElement);
    });
    searchResults.classList.remove('hidden');
  } else {
    const noResultElement = document.createElement('div');
    noResultElement.classList.add('p-2', 'text-white');
    noResultElement.textContent = 'No guarantor found';
    searchResults.appendChild(noResultElement);
    searchResults.classList.remove('hidden');
  }
});

document.addEventListener('click', function (event) {
  if (!searchResults.contains(event.target) && event.target !== searchInput) {
    searchResults.innerHTML = '';
    searchResults.classList.add('hidden');
  }
});