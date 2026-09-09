document.addEventListener("DOMContentLoaded", () => {
    const wrapperButton = document.querySelector(".b4");
    const popupOverlay = document.getElementById("popupOverlay");
    const exitButton = document.getElementById("exitButton");

    wrapperButton.addEventListener("click", () => {
        popupOverlay.classList.add("active");
    });

    exitButton.addEventListener("click", () => {
        popupOverlay.classList.remove("active");
    });

    // Close the popup if the overlay is clicked
    popupOverlay.addEventListener("click", (e) => {
        if (e.target === popupOverlay) {
            popupOverlay.classList.remove("active");
        }
    });
});
