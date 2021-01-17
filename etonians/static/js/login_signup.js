// Redirects user to the login form, if user previously submitted it.
function checkLoginPage() {
  const isLoginPage = document.getElementById('is-login-page');

  if (isLoginPage && isLoginPage.innerHTML == 'true') {
    const userAuthContainer = document.querySelector('.login-signup-container');
    userAuthContainer.classList.add('scene-switch');
    document.title = 'Log In | Etonians';
  }
}

window.onload = function() {
  checkLoginPage();
  initFlashedMessages();
}

const login_signup_page = () => {
  const loginButton = document.getElementById('login-btn');

  // Checks if user wants to switch to login.
  loginButton.addEventListener('click', () => {
    const userAuthContainer = document.querySelector('.login-signup-container');
    userAuthContainer.classList.add('scene-switch');
    document.title = 'Log In | Etonians';
  });

  const signUpButton = document.getElementById('signup-btn');

  // Checks if user wants to switch to sign up.
  signUpButton.addEventListener('click', () => {
    const userAuthContainer = document.querySelector('.login-signup-container');
    userAuthContainer.classList.remove('scene-switch');
    document.title = 'Sign Up | Etonians';
  });

  const passwordInputFields = document.querySelectorAll('.password-field > .text-input');

  // ability for users to show and hide password input
  passwordInputFields.forEach(item => {
    const showPasswordButton = item.parentElement.querySelector('.show-password');

    showPasswordButton.addEventListener('click', () => {
      if (showPasswordButton.classList.contains('fa-eye')) {
        showPasswordButton.classList.remove('fa-eye')
        showPasswordButton.classList.add('fa-eye-slash');

        item.type = 'text';
      } else {
        showPasswordButton.classList.remove('fa-eye-slash');
        showPasswordButton.classList.add('fa-eye');

        item.type = 'password';
      }
    });
  });
}

login_signup_page();