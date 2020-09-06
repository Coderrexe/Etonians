$(window).scroll(function() {
    let scroll = $(window).scrollTop();

    if (scroll >= 10) {
        $(".navbar-js").addClass("nav-scroll");
    } else {
        $(".navbar-js").removeClass("nav-scroll");
    }
});

// const likeBtn = document.getElementById("likes");

// function incrementValue() {
//     var value = parseInt(likeBtn.value, 10);
//     value = isNaN(value) ? 0 : value;
//     value++;
//     likeBtn.value = value;
//     document.write(value);
// }
