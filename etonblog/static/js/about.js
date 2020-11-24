// navbar toggler
function navbarToggle() {
    const navbarToggler = document.querySelector('.navbar-toggler');

    navbarToggler.addEventListener('click', () => {
        navbarToggler.classList.toggle('toggle');
    });
}

navbarToggle();
