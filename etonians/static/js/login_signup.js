const loginButton = document.getElementById('login-btn');
const signUpButton = document.getElementById('signup-btn');
const userAuthContainer = document.querySelector('.login-signup-container');

const flashedMessage = document.querySelector('.flashed-message');
const closeButton = document.querySelector('.close-button');

window.onload = function() {
    const isLoginPage = document.getElementById('is-login-page');

    if (isLoginPage.innerHTML == 'true') {
        userAuthContainer.classList.add('scene-switch');
        document.title = 'Log In | Etonians';
    }

    if (flashedMessage.classList.contains('active')) {
        flashedMessage.classList.remove('active');
        flashedMessage.classList.add('show');
    }
}

loginButton.addEventListener('click', function() {
    userAuthContainer.classList.add('scene-switch');
    document.title = 'Log In | Etonians';
});

signUpButton.addEventListener('click', function() {
    userAuthContainer.classList.remove('scene-switch');
    document.title = 'Sign Up | Etonians';
});

closeButton.addEventListener('click', function() {
    flashedMessage.classList.remove('show');
});
