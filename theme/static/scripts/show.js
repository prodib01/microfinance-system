document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('password-toggle');
    const iconEye = document.getElementById('icon-eye');

    passwordToggle.addEventListener('click', function () {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      iconEye.classList.toggle("fi fi-rr-eye-crossed", type === 'text');
      iconEye.classList.toggle("fi fi-rr-eye", type === 'password');
    });
  });