// fixes material icons glitch
window.addEventListener('load', function() {
    const materialIcons = document.querySelectorAll('.material-icons, .material-icons-outlined');

    materialIcons.forEach((icon) => {
        icon.style.opacity = 1;
    });
});

// user profile picture dropdown menu
const menuToggler = document.querySelector('.profile');
const menu = document.querySelector('.menu');
const menuContainer = document.querySelector('.menu-container');

menuToggler.addEventListener('click', function() {
    menu.classList.toggle('active');
});

document.addEventListener('click', function(event) {
    if (!menuContainer.contains(event.target)) {
        menu.classList.remove('active');
    }
});

// "back" button when viewing a post
function historyBack() {
    if (document.referrer != window.location.href) {
        history.back();
    } else {
        window.location.replace('/home/');
    }
}

// fixes popup modal fullscreen glitch
function modalResponsive() {
    let windowWidth = window.innerWidth;
    const textFieldModals = document.querySelectorAll('.text-field-modal-dialog');

    if (windowWidth <= 570) {
        textFieldModals.forEach((modal) => {
            modal.classList.remove('modal-dialog-scrollable');
        });
    } else if (windowWidth > 570) {
        textFieldModals.forEach((modal) => {
            modal.classList.add('modal-dialog-scrollable');
        });
    }
}

modalResponsive();
window.addEventListener('resize', modalResponsive);
