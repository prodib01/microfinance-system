function previewImage(event) {
    const fileInput = event.target;
    const files = fileInput.files;

    for (const file of files) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const imageSrc = e.target.result;
            displayImagePreview(imageSrc);
        };

        reader.readAsDataURL(file);
    }
    
    // fileInput.value = null;
}

function displayImagePreview(imageSrc) {
    const container = document.getElementById('image-preview-container');

    const previewContainer = document.createElement('div');
    previewContainer.className = 'image-preview';

    const img = document.createElement('img');
    img.src = imageSrc;

    const cancelButton = document.createElement('button');
    cancelButton.className = 'cancel-button';
    cancelButton.textContent = 'X';
    cancelButton.onclick = function () {
        container.removeChild(previewContainer);
    };

    previewContainer.appendChild(img);
    previewContainer.appendChild(cancelButton);

    container.appendChild(previewContainer);
}
