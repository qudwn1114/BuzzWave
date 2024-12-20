const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// 헤더 메뉴 클릭 이벤트
const header = document.querySelector(".header");
const headerNavLinks = document.querySelectorAll(".header_nav a");
const mainSections = document.querySelectorAll("section");

window.addEventListener("DOMContentLoaded", () => {
    const hash = window.location.hash;
    if (hash) {
        const target = document.querySelector(
            `section[data-scroll=${hash.replace("#", "")}`
        );
        const targetTop = target.offsetTop - header.clientHeight;
        window.scrollTo({
            top: targetTop,
            behavior: "smooth",
        });
    }
});

headerNavLinks.forEach((item) => {
    item.addEventListener("click", (e) => {
        if (item.getAttribute("href").charAt(0) !== "#") return;

        e.preventDefault();

        const mainSection = document.querySelector(
            `section[data-scroll=${item.getAttribute("href").replace("#", "")}]`
        );

        window.scrollTo({
            top: mainSection.offsetTop - header.clientHeight,
            behavior: "smooth",
        });
    });
});