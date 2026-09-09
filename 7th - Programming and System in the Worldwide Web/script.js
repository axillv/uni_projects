
//mobile menu leitourgia
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const overlay = document.getElementById('overlay');
    const closeOverlay = document.getElementById('closeOverlay');
    const overlayLoginButton = document.getElementById('overlayLoginButton');

    menuToggle.addEventListener('click', function() {
        if (overlay.style.display === 'flex') {
            overlay.style.display = 'none';
        } else {
            overlay.style.display = 'flex';
        }
    });

    closeOverlay.addEventListener('click', function() {
        overlay.style.display = 'none';
    });

    // Close overlay when clicking outside the content
    overlay.addEventListener('click', function(event) {
        if (event.target === overlay) {
            overlay.style.display = 'none';
        }
    });

    // Optional: Add functionality to overlay login button if needed
    overlayLoginButton.addEventListener('click', function() {
        alert('Login button clicked inside overlay');
    });
});


//savvatou login
document.addEventListener("DOMContentLoaded", () => {
    const wrapperButton = document.querySelector(".logBT");
    const exitButton = document.getElementById("exitButton5");
    const cont2 = document.getElementById("contF");
    
    wrapperButton.addEventListener("click", () => {
        if (cont2.style.display === 'none' ) {
            cont2.style.display = 'grid';
        } else {
            cont2.style.display = 'none';
        }
    });

    exitButton.addEventListener("click", () => {
        cont2.style.display = 'none';
    });

    //gia mobile version
    const wrapperButton2 = document.querySelector(".customB");
    
    wrapperButton2.addEventListener("click", () => {
        if (cont2.style.display === 'none' ) {
            cont2.style.display = 'grid';
        } else {
            cont2.style.display = 'none';
        }
    });

    exitButton.addEventListener("click", () => {
        cont2.style.display = 'none';
    });

});