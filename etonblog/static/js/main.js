$(window).scroll(function() {
    const body = document.querySelector("body");
    body.scrollLeft = 0;
});

const navbar = () => {
    const navbarToggler = document.getElementById("navbar-toggler");
    const nav = document.querySelector(".nav-links");
    const navLinks = document.querySelectorAll(".nav-links li");
    const main = document.querySelector("main");

    // toggles navbar on mobile devices
    navbarToggler.addEventListener("click", () => {
        nav.classList.toggle("nav-toggled");
        main.classList.toggle("darken");

        // animates navbar links on mobile devices
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = ``;
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });

        // navbar toggler animation
        navbarToggler.classList.toggle("toggle");
    });
};

const app = () => {
    navbar();
};

app();
