const navbar = () => {
    const navbarToggler = document.querySelector(".navbar-toggler");

    navbarToggler.addEventListener("click", () => {
        navbarToggler.classList.toggle("toggle");
    });
}

navbar();
