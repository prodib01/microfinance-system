const users = [
  { id: 1, name: 'John Doe', accountNumber: '123456789' },
  { id: 2, name: 'Jane Doe', accountNumber: '987654321' },
  { id: 3, name: 'Alice Smith', accountNumber: '555666777' },
  { id: 4, name: 'Bob Johnson', accountNumber: '999888777' }
];

function renderDropdownResults(results) {
  const dropdownResultsDiv = document.getElementById('dropdownResults');
  dropdownResultsDiv.innerHTML = '';

  results.forEach(user => {
    const userLink = document.createElement('a');
    userLink.textContent = user.name + ' - ' + user.accountNumber;
    userLink.href = '#';
    userLink.classList.add('block', 'py-2', 'px-4', 'hover:bg-gray-800', 'cursor-pointer');

    userLink.addEventListener('click', () => {
      document.getElementById('selectedUserName').textContent = user.name;
      document.getElementById('selectedUserAccountNumber').textContent = user.accountNumber;
      document.getElementById('selectedUser').classList.remove('hidden');
      document.getElementById('searchInput').value = '';
      document.getElementById('selectedUserId').value = user.id;
      document.getElementById('selectedUserAccountId').value = user.accountNumber;
      dropdownResultsDiv.style.display = 'none';
    });

    dropdownResultsDiv.appendChild(userLink);
  });

  if (results.length > 0) {
    dropdownResultsDiv.style.display = 'block';
  } else {
    dropdownResultsDiv.style.display = 'none';
  }
}

function handleSearch() {
  const searchInput = document.getElementById('searchInput');
  const searchTerm = searchInput.value.toLowerCase();
  const results = users.filter(user => user.name.toLowerCase().includes(searchTerm) || user.accountNumber.includes(searchTerm));
  renderDropdownResults(results);
}

document.getElementById('searchInput').addEventListener('input', handleSearch);

document.addEventListener('click', function (event) {
  const dropdownResultsDiv = document.getElementById('dropdownResults');
  if (!event.target.matches('#searchInput')) {
    dropdownResultsDiv.style.display = 'none';
  }
});

document.getElementById('cancelBtn').addEventListener('click', () => {
  document.getElementById('selectedUserName').textContent = '';
  document.getElementById('selectedUserAccountNumber').textContent = '';
  document.getElementById('selectedUser').classList.add('hidden');
  document.getElementById('selectedUserId').value = '';
  document.getElementById('selectedUserAccountId').value = '';
});