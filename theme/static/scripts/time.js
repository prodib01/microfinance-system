document.addEventListener('DOMContentLoaded', function () {
    const currentHour = new Date().getHours();

    const greetingElement = document.getElementById('time');

    if (currentHour >= 5 && currentHour < 12) {
      greetingElement.textContent = 'Good morning!';
    } else if (currentHour >= 12 && currentHour < 18) {
      greetingElement.textContent = 'Good afternoon!';
    } else {
      greetingElement.textContent = 'Good evening!';
    }
  });