// user profile picture dropdown menu
const menuToggler = document.querySelector('.profile');
const menu = document.querySelector('.menu');

menuToggler.addEventListener('click', function() {
    menu.classList.toggle('active');
});

document.addEventListener('click', function(event) {
    if (!menuToggler.contains(event.target)) {
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
