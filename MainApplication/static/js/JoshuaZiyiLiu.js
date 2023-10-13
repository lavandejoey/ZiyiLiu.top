// auto fresh the page in 2seconds
num_second = 5;
// timeout = num_second * 1000;
// for (let i = 1; i < 100; i++) {
//     setTimeout(function () {
//         window.location.reload();
//     }, timeout);
// }

document.addEventListener('DOMContentLoaded', function () {
    // class ".at-top" to header
    const header = document.getElementsByTagName('header')[0];
    if (header) {
        // get current scroll position and add class
        if (window.scrollY === 0) {
            header.classList.add('at-top');
        }
        window.addEventListener('scroll', function () {
            if (window.scrollY === 0) {
                header.classList.add('at-top');
            } else {
                header.classList.remove('at-top');
            }
        });
    }

    // Blinking caret
    const caret = document.getElementById('caret');
    if (caret) {
        setInterval(function () {
            caret.classList.toggle('invisible');
        }, 500);
    }
});