const navbar = () => {
  const searchBarContainer = document.querySelector('.top-navbar .search-bar-container');
  const searchBar = document.querySelector('.top-navbar .search-bar');
  const searchButtonBack = document.querySelector('.top-navbar .search-bar .back');
  const navLinks = document.querySelector('.top-navbar > .nav-links');
  const searchInput = document.querySelector('.search-bar > form > .text-input');

  searchBarContainer.addEventListener('click', () => {
    searchBar.classList.add('active');
    searchInput.focus();
  });

  searchButtonBack.addEventListener('click', () => {
    searchBar.classList.remove('active');
    searchInput.blur();
  });

  document.addEventListener('click', event => {
    if (!navLinks.contains(event.target)) {
      searchBar.classList.remove('active');
      searchInput.blur();
    }
  });
}

navbar();
