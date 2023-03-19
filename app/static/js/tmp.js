// setInterval(function () {
//     location.reload();
// }, 10000); // reloads the page every 5 seconds

/**
 * Typewriter simulation
 * 1. caret blinking
 * 2. when website load, retype the inner element
 * 3. when hover on the elements of navbar, retype the inner element
 * 4. type the title and greetings when load the page
 */
const caretDiv = document.querySelectorAll(".nav-link");
for (let idx = 0; idx < caretDiv.length; idx++) {
    const tobeType = caretDiv[idx].querySelector("span.hover-typewriter");
    const caret = caretDiv[idx].querySelector("span.hover-blink-caret");
    let typing = false;
    let deleting = false;
    const content = tobeType.innerHTML;
    let currentPos = 0;
    let typingInterval = null;
    let deletingInterval = null;
    let isVisible = false;

    tobeType.innerHTML = "";
    caret.innerHTML = "";
    // blinking caret
    setInterval(() => {
        if (isVisible === true) {
            isVisible = false;
            caret.style.visibility = "hidden";
        } else {
            isVisible = true;
            caret.style.visibility = "visible";
        }
    }, 600);
    // for the context of nav-link
    caretDiv[idx].addEventListener("mouseenter", () => {
        tobeType.classList.remove("visually-hidden");
        clearInterval(deletingInterval);
        deleting = false;
        typing = true;
        caret.innerHTML = "|";
        typingInterval = setInterval(() => {
            if (currentPos < content.length) {
                tobeType.innerHTML += content[currentPos];
                currentPos++;
            } else {
                clearInterval(typingInterval);
                typing = false;
                deleting = true;
            }
        }, 80);
    });

    caretDiv[idx].addEventListener("mouseleave", () => {
        clearInterval(typingInterval);
        typing = false;
        deleting = true;
        deletingInterval = setInterval(() => {
            if (currentPos > 0) {
                tobeType.innerHTML = tobeType.innerHTML.slice(0, -1);
                currentPos--;
            } else {
                caret.innerHTML = "";
                //caret.classList.add("visually-hidden");
                tobeType.classList.add("visually-hidden");
                clearInterval(deletingInterval);
                deleting = false;
            }
        }, 10);
    });
}


/**
 * navbar transition
 */
// Get the navbar element
let navbar = document.querySelector("header");
// Get the current scroll position
let prevScrollPos = window.pageYOffset;
// Listen for the scroll event
window.onscroll = function () {
    let currentScrollPos = window.pageYOffset;
    navbar.style.top = "-" + (navbar.offsetHeight + 5) + "px";
    // Check if scrolling down
    if (prevScrollPos > currentScrollPos || currentScrollPos === 0) {
        // Show the navbar
        navbar.style.top = "0";
    } else {
        // Hide the navbar
        navbar.style.top = "-" + (navbar.offsetHeight + 5) + "px";
    }
    // Update the previous scroll position
    prevScrollPos = currentScrollPos;
};

/**
 * The name opacity and change of
 */
const text1 = document.getElementById('text-1');
const text2 = document.getElementById('text-2');
const text3 = document.getElementById('text-3');


window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition >= 200) {
        text1.classList.add('expanded');
        text2.classList.add('expanded');
        text3.classList.add('expanded');
    } else {
        text1.classList.remove('expanded');
        text2.classList.remove('expanded');
        text3.classList.remove('expanded');
    }
});
