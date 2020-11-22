function historyBack() {
    if (document.referrer != window.location.href) {
        history.back();
    } else {
        window.location.replace('/home/');
    }
}
