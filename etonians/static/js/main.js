// Fixes Material Icons text glitch.
function materialIconsOpacity() {
  const materialIcons = document.querySelectorAll('.material-icons, .material-icons-outlined');

  materialIcons.forEach(icon => {
    icon.style.opacity = 1;
  });
}

window.onload = function() {
  materialIconsOpacity();
  initFlashedMessages();
};

// Back button when viewing a post.
function historyBack() {
  if (document.referrer != window.location.href) {
    history.back();
  } else {
    window.location.replace('/home/');
  }
}

const main = () => {
  // User profile picture dropdown menu.
  const menuToggler = document.querySelector('.profile');
  const menu = document.querySelector('.menu');
  const menuContainer = document.querySelector('.menu-container');

  menuToggler.addEventListener('click', () => {
    menu.classList.toggle('active');
  });

  document.addEventListener('click', event => {
    if (!menuContainer.contains(event.target)) {
      menu.classList.remove('active');
    }
  });

  // Fixes popup modal fullscreen glitch.
  const modalResponsive = () => {
    let windowWidth = window.innerWidth;
    const textFieldModals = document.querySelectorAll('.text-field-modal-dialog');

    if (windowWidth <= 570) {
      textFieldModals.forEach(modal => {
        modal.classList.remove('modal-dialog-scrollable');
      });
    } else if (windowWidth > 570) {
      textFieldModals.forEach(modal => {
        modal.classList.add('modal-dialog-scrollable');
      });
    }
  }

  modalResponsive();
  window.addEventListener('resize', modalResponsive);
}

main();
