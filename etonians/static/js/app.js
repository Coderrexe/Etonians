if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
  .then(registration => {
    console.log('Service worker registered!');
    console.log(registration);
    return registration;
  }).catch(error => {
    console.log('An error occurred.')
    console.log(error);
  });
}
