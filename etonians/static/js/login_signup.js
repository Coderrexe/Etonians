// page animation
const loginButton = document.getElementById('login-btn');
const signUpButton = document.getElementById('signup-btn');
const userAuthContainer = document.querySelector('.login-signup-container');

loginButton.addEventListener('click', function() {
  userAuthContainer.classList.add('scene-switch');
  document.title = 'Log In | Etonians';
});

signUpButton.addEventListener('click', function() {
  userAuthContainer.classList.remove('scene-switch');
  document.title = 'Sign Up | Etonians';
});
