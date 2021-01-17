// When a page loads, shows the flashed messages sent from Flask back-end.
function initFlashedMessages() {
  const flashedMessage = document.querySelector('.flashed-message');

  if (flashedMessage && flashedMessage.classList.contains('active')) {
    flashedMessage.classList.remove('active');
    flashedMessage.classList.add('show');
  }
}

const closeButton = document.querySelector('.close-button');

// Checks if user closes the flashed message.
if (closeButton) {
  closeButton.addEventListener('click', () => {
    const flashedMessage = document.querySelector('.flashed-message');
    flashedMessage.classList.remove('show');
  });
}
