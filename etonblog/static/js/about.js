window.addEventListener("scroll", function() {
    let navbarJs = document.querySelector(".navbar-js");
    navbarJs.classList.toggle("nav-scroll", window.scrollY > 0);
});

const navbar = () => {
    const navbarToggler = document.querySelector(".navbar-toggler");

    navbarToggler.addEventListener("click", () => {
        navbarToggler.classList.toggle("toggle");
    });
};

navbar();
