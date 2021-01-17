// Navbar expand button in mobile view.
function navbarToggle() {
  const navbarToggler = document.querySelector('.navbar-toggler');

  navbarToggler.addEventListener('click', () => {
    navbarToggler.classList.toggle('toggle');
  });
}

navbarToggle();
