document.addEventListener('DOMContentLoaded', function () {
    const selectOption = document.getElementById('options');
    const additionalFieldsContainer = document.getElementById('married');
  
    selectOption.addEventListener('change', function () {
      if (selectOption.value === 'married') {
        displayAdditionalFieldsForOption1();
      } else {
        hideAdditionalFields();
      }
    });
  
    function displayAdditionalFieldsForOption1() {
      additionalFieldsContainer.classList.remove('hidden');
    }
  
    function hideAdditionalFields() {
      additionalFieldsContainer.classList.add('hidden');
    }
  });
  