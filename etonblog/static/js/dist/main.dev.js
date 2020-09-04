"use strict";

$(window).scroll(function () {
  var scroll = $(window).scrollTop();

  if (scroll >= 10) {
    $(".navbar-js").addClass("nav-scroll");
  } else {
    $(".navbar-js").removeClass("nav-scroll");
  }
});