// Function to set or reset a cookie
function setCookie(name, value, minutes) {
    var expires = "";
    if (minutes) {
        var date = new Date();
        date.setTime(date.getTime() + (minutes * 60 * 1000)); // Convert minutes to milliseconds
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

// Function to reset the session cookie when the user is active
function extendSession() {
    setCookie('admin_session', 'active', 20);  // Reset session for another 20 minutes
}

// Add event listeners for user activity (mousemove, keypress, click)
window.addEventListener('mousemove', extendSession);
window.addEventListener('keypress', extendSession);
window.addEventListener('click', extendSession);

// Function to continuously check if the session cookie exists and redirect if missing
function checkSession() {
    var sessionCookie = getCookie('admin_session');
    var adminID = localStorage.getItem('admin_id');

    if (!sessionCookie || !adminID) {
        // If the session cookie is missing or expired, redirect to login
        window.location.href = '../start.html';
    }
}

// Check the session immediately when the page loads
window.onload = function() {
    checkSession();  // Initial check

    // Set an interval to check the session every minute (60000 milliseconds)
    setInterval(checkSession, 60000);  // Check every 1 minute
};

// Function to get a cookie by name
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Logout functionality
document.getElementById('loggout').addEventListener('click', function (e) {
    e.preventDefault();

    // Remove the session cookie and admin ID from localStorage
    document.cookie = "admin_session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.removeEventListener('mousemove', extendSession);
    window.removeEventListener('keypress', extendSession);
    window.removeEventListener('click', extendSession);
    localStorage.removeItem('admin_id');
    localStorage.removeItem('role');

    // Redirect to login page
    window.location.href = '../start.html';
});



// Optional: Open popup on page load
// openPopup();
document.getElementById('stockManage').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    manageStock();
});
document.getElementById('stockStatus').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    showStock();
});
document.getElementById('statistikaShow').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    showStatistika();
});
document.getElementById('newsCreate').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    newAithma();
});
document.getElementById('rescuerCreate').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    newDiasostis();
});


//leitourgies parathiron apo to menu
function newAithma() {
    //to parakato pernaei
    var contentSection = document.getElementById('newAithmata');
    //ta parakato kovontai
    var mapContainer = document.getElementById('mapContainerI');
    var contentSectionX = document.getElementById('newDiasosths');
    var contentSectionX2 = document.getElementById('statistikoulia');
    var contentSectionX3 = document.getElementById('chartContainer');
    var contentSectionX4 = document.getElementById('stockW');
    var contentSectionX5 = document.getElementById('categoryItemForm');
    var contentSectionX6 = document.getElementById('simpleTextFieldForm');
    var contentSectionX7 = document.getElementById('uploadFileForm');
    //pernaei
    contentSection.style.display = 'block';
    //kovontai
    mapContainer.style.display = 'none';
    contentSectionX.style.display ='none';
    contentSectionX2.style.display ='none';
    contentSectionX3.style.display ='none';
    contentSectionX4.style.display ='none';
    contentSectionX5.style.display ='none';
    contentSectionX6.style.display ='none';
    contentSectionX7.style.display ='none';
}

function newDiasostis() {
    //to parakato pernaei
    var contentSection = document.getElementById('newDiasosths');
    //ta parakato kruvontai
    var mapContainer = document.getElementById('mapContainerI');
    var contentSectionX = document.getElementById('newAithmata');
    var contentSectionX2 = document.getElementById('statistikoulia');
    var contentSectionX3 = document.getElementById('chartContainer');
    var contentSectionX4 = document.getElementById('stockW');
    var contentSectionX5 = document.getElementById('categoryItemForm');
    var contentSectionX6 = document.getElementById('simpleTextFieldForm');
    var contentSectionX7 = document.getElementById('uploadFileForm');
    //pernaei
    contentSection.style.display = 'block';
    //kovontai
    contentSectionX.style.display ='none';
    contentSectionX2.style.display ='none';
    contentSectionX3.style.display ='none';
    contentSectionX4.style.display ='none';
    contentSectionX5.style.display ='none';
    contentSectionX6.style.display ='none';
    contentSectionX7.style.display ='none';
    mapContainer.style.display = 'none';
}

function showStatistika() {
    //to parakato pernaei
    var contentSection = document.getElementById('statistikoulia');
    //ta parakato kovontai
    var mapContainer = document.getElementById('mapContainerI');
    var contentSectionX = document.getElementById('newDiasosths');
    var contentSectionX2 = document.getElementById('newAithmata');
    var contentSectionX4 = document.getElementById('stockW');
    var contentSectionX5 = document.getElementById('categoryItemForm');
    var contentSectionX6 = document.getElementById('simpleTextFieldForm');
    var contentSectionX7 = document.getElementById('uploadFileForm');
    //pernaei
    contentSection.style.display = 'block';
    //kovontai
    mapContainer.style.display = 'none';
    contentSectionX.style.display ='none';
    contentSectionX2.style.display ='none';
    contentSectionX4.style.display ='none';
    contentSectionX5.style.display ='none';
    contentSectionX6.style.display ='none';
    contentSectionX7.style.display ='none';
}

function showStock() {
    //to parakato pernaei
    var contentSection = document.getElementById('stockW');
    //ta parakato kruvontai
    var mapContainer = document.getElementById('mapContainerI');
    var contentSectionX = document.getElementById('newAithmata');
    var contentSectionX2 = document.getElementById('statistikoulia');
    var contentSectionX3 = document.getElementById('chartContainer');
    var contentSectionX4 = document.getElementById('newDiasosths');
    var contentSectionX5 = document.getElementById('categoryItemForm');
    var contentSectionX6 = document.getElementById('simpleTextFieldForm');
    var contentSectionX7 = document.getElementById('uploadFileForm');
    
    //pernaei
    contentSection.style.display = 'block';
    //kovontai
    contentSectionX.style.display ='none';
    contentSectionX2.style.display ='none';
    contentSectionX3.style.display ='none';
    contentSectionX4.style.display ='none';
    mapContainer.style.display = 'none';
    contentSectionX5.style.display ='none';
    contentSectionX6.style.display ='none';
    contentSectionX7.style.display ='none';
}


function manageStock() {
    //to parakato pernaei
    var contentSection = document.getElementById('stockW');
    //ta parakato kruvontai
    var mapContainer = document.getElementById('mapContainerI');
    var contentSectionX = document.getElementById('newAithmata');
    var contentSectionX2 = document.getElementById('statistikoulia');
    var contentSectionX3 = document.getElementById('chartContainer');
    var contentSectionX4 = document.getElementById('newDiasosths');
    var contentSectionX5 = document.getElementById('categoryItemForm');
    var contentSectionX6 = document.getElementById('simpleTextFieldForm');
    var contentSectionX7 = document.getElementById('uploadFileForm');
    
    //pernaei
    contentSectionX5.style.display ='block';
    contentSectionX6.style.display ='block';
    contentSectionX7.style.display ='block';
    
    //kovontai
    contentSectionX.style.display ='none';
    contentSectionX2.style.display ='none';
    contentSectionX3.style.display ='none';
    contentSectionX4.style.display ='none';
    mapContainer.style.display = 'none';
    contentSection.style.display = 'none';
}
//anakateuthinsi sthn admin othoni
document.getElementById('logoF').addEventListener('click', function(e) {
    e.preventDefault();
    var mapContainer = document.getElementById('mapContainerI');
    var contentSectionX = document.getElementById('newAithmata');
    var contentSectionX2 = document.getElementById('statistikoulia');
    var contentSection = document.getElementById('newDiasosths');
    var contentSectionX3 = document.getElementById('chartContainer');
    var contentSectionX4 = document.getElementById('stockW');
    var contentSectionX5 = document.getElementById('categoryItemForm');
    var contentSectionX6 = document.getElementById('simpleTextFieldForm');
    var contentSectionX7 = document.getElementById('uploadFileForm');

    mapContainer.style.display = 'block';
    contentSection.style.display = 'none';
    contentSectionX.style.display = 'none';
    contentSectionX2.style.display = 'none';
    contentSectionX3.style.display = 'none';
    contentSectionX4.style.display = 'none';
    contentSectionX5.style.display ='none';
    contentSectionX6.style.display ='none';
    contentSectionX7.style.display ='none';
});


//mobile version
// Add this to your mapScript.js

function toggleMenu() {
    const menuBar = document.querySelector('.menu-bar');
    menuBar.style.display = menuBar.style.display === 'flex' ? 'none' : 'flex';
}

document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item-container');

    menuItems.forEach(item => {
        item.addEventListener('click', function(event) {
            if (window.innerWidth <= 768) {
                event.stopPropagation(); // Prevent the click from closing the menu
                menuItems.forEach(el => el !== this && el.classList.remove('active'));
                this.classList.toggle('active');
            }
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
        if (window.innerWidth <= 768) {
            menuItems.forEach(item => item.classList.remove('active'));
        }
    });
});

const draggableBox = document.getElementById("draggableBox");

let isDragging = false;
let initialX, initialY, offsetX = 0, offsetY = 0;

draggableBox.addEventListener('mousedown', startDrag);
document.addEventListener('mousemove', drag);
document.addEventListener('mouseup', stopDrag);

function startDrag(e) {
    isDragging = true;
    const event = e.type === 'touchstart' ? e.touches[0] : e;
    initialX = event.clientX - offsetX;
    initialY = event.clientY - offsetY;

    draggableBox.style.cursor = 'grabbing';
}

function drag(e) {
    if (!isDragging) return;
    
    const event = e.type === 'touchmove' ? e.touches[0] : e;
    offsetX = event.clientX - initialX;
    offsetY = event.clientY - initialY;

    draggableBox.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
}

function stopDrag() {
    isDragging = false;
    draggableBox.style.cursor = 'grab';
}

// Table sorting!
// https://stackoverflow.com/questions/14267781/sorting-html-table-with-javascript
const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

// Add event listeners to each header for sorting
document.querySelectorAll('th').forEach(th => th.addEventListener('click', function() {
    if (th.classList.contains('no-sort')) return; // Skip sorting for this column

    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    const index = Array.from(th.parentNode.children).indexOf(th);
    const asc = this.asc = !this.asc;

    // Remove sort indicators from all headers
    document.querySelectorAll('th').forEach(header => {
        header.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort indicator to the clicked header
    th.classList.add(asc ? 'sort-asc' : 'sort-desc');

    Array.from(tbody.querySelectorAll('tr'))
        .sort(comparer(index, asc))
        .forEach(tr => tbody.appendChild(tr));
}));