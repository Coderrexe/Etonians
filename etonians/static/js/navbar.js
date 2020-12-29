const searchBarContainer = document.querySelector('.top-navbar .search-bar-container');
const searchBar = document.querySelector('.top-navbar .search-bar');
const searchButtonBack = document.querySelector('.top-navbar .search-bar .back');
const navLinks = document.querySelector('.top-navbar > .nav-links')

searchBarContainer.addEventListener('click', function() {
    searchBar.classList.add('active');
});

searchButtonBack.addEventListener('click', function() {
    searchBar.classList.remove('active');
});

document.addEventListener('click', function(event) {
    if (!navLinks.contains(event.target)) {
        searchBar.classList.remove('active');
    }
});
