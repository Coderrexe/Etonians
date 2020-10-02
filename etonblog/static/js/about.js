$(window).scroll(function() {
    let scroll = $(window).scrollTop();

    if (scroll >= 10) {
        $(".navbar-js").addClass("nav-scroll");
    } else {
        $(".navbar-js").removeClass("nav-scroll");
    }
});

const navbar = () => {
    const navbarToggler = document.querySelector(".navbar-toggler");

    navbarToggler.addEventListener("click", () => {
        navbarToggler.classList.toggle("toggle");
    });
};

const app = () => {
    navbar();
};

app();
