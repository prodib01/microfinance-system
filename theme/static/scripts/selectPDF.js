const addedFiles = [];
function addFile() {
  const fileInput = document.getElementById('fileInput');
  const fileList = document.getElementById('fileList');

  Array.from(fileInput.files).forEach(file => {
    if (!addedFiles.includes(file.name)) {
      const listItem = document.createElement('li');
      listItem.textContent = file.name;
      listItem.classList.add('mb-2')

      const cancelBtn = document.createElement('button');
      cancelBtn.textContent = 'x';
      cancelBtn.classList.add('ml-2', 'bg-red-500', 'hover:bg-red-700', 'text-white', 'font-bold', 'px-2', 'rounded-full');
      cancelBtn.onclick = () => {
        listItem.remove();
        fileInput.value = null;
        const index = addedFiles.indexOf(file.name);
        if (index !== -1) {
          addedFiles.splice(index, 1);
        }
      };
      listItem.appendChild(cancelBtn);

      fileList.appendChild(listItem);
      addedFiles.push(file.name);
    } else {
      alert('This file has already been added.');
    }
  });
}