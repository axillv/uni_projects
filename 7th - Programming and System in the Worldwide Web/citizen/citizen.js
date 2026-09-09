/**
 * Cookies management
 */
function checkSession() {
    var sessionCookie = getCookie('citizen_session');
    var citizen_id = localStorage.getItem('citizen_id');

    if (!sessionCookie || !citizen_id) {
        // If the session cookie is missing or expired, redirect to login
        localStorage.removeItem('citizen_id');
        window.location.href = '../start.html';
    }
}

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

function setCookie(name, value, minutes) {
    var expires = "";
    if (minutes) {
        var date = new Date();
        date.setTime(date.getTime() + (minutes * 60 * 1000)); // Convert minutes to milliseconds
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function extendSession() {
    setCookie('citizen_session', 'active', sessionTime);  // Reset session for another 20 minutes
}

/**
 * Global variables
 */
var requestsData;
var offersData;
var announcementsData;
var allItemCategories;
var allItems;
var expiryDates = { "Requests": null, "Offers": null, "Announcements": null, "Categories": null, "Items": null };
const expiryTime = 60000; // 1 minute in milliseconds
const sessionTime = 20 // 20 minutes

/**
 * Event Listeners
 */
// Add event listeners for user activity (mousemove, keypress, click)
window.addEventListener('mousemove', extendSession);
window.addEventListener('keypress', extendSession);
window.addEventListener('click', extendSession);

const newRequestElement = document.getElementById('newRequest');
const categoryList = newRequestElement.querySelector('#category');
categoryList.addEventListener('change', function () {
    allItems.then(items => {
        populateRequestItems(items);
        newRequestElement.querySelector('#searchStock').value = ''; //empty selected item
    });
});

const requestsScreenButton = document.getElementById('requestsScreen');
requestsScreenButton.addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    showRequestsScreen();
});

const offersScreenButton = document.getElementById('offersScreen');
offersScreenButton.addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior
    showOffersScreen();
});

const logoutButton = document.getElementById('logout');
logoutButton.addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior

    document.cookie = "citizen_session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    localStorage.removeItem('citizen_id');
    localStorage.removeItem('role');

    window.location.href = '../start.html';
});

const requestTable = document.getElementById('newRequest');
const requestSubmitButton = requestTable.querySelector('.btn.submit');
requestSubmitButton.addEventListener('click', function (e) {
    var selectedItemName = requestTable.querySelector('#searchStock').value;
    var numOfPeople = requestTable.querySelector('#peopleNumb').value;

    createRequest(selectedItemName, numOfPeople);
});

const offerTable = document.getElementById('offerG');
const offerSubmitButton = offerTable.querySelector('.btn.submit');
offerSubmitButton.addEventListener('click', function (e) {
    var filledCheckboxes = Array.from(offerTable.querySelectorAll('input[type=checkbox]'))
        .filter(input => input.checked);

    // Get parent tr, select third column (which contains item name)
    var selectedItemNames = Array.from(filledCheckboxes).map(checkbox => {
        var row = checkbox.closest('tr');
        return row.querySelectorAll('td')[2].textContent;
    });

    // same as above for quantities
    var quantities = Array.from(filledCheckboxes).map(checkbox => {
        var row = checkbox.closest('tr');
        return row.querySelectorAll('td')[3].textContent;
    });

    createOffer(selectedItemNames, quantities);
});

// Table sorting!
// https://stackoverflow.com/questions/14267781/sorting-html-table-with-javascript
const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
)(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

// Add event listeners to each header for sorting
document.querySelectorAll('th').forEach(th => th.addEventListener('click', function () {
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

/**
 * Mobile frontend  //todo: this doesn't do anything??
 */
const menuItems = document.querySelectorAll('.menu-item');
menuItems.forEach(item => {
    item.addEventListener('click', function (event) {
        if (window.innerWidth <= 768) {
            event.stopPropagation(); // Prevent the click from closing the menu
            menuItems.forEach(el => el !== this && el.classList.remove('active'));
            this.classList.toggle('active');
        }
    });
});

// Close dropdown when clicking outside
document.addEventListener('click', function () {
    if (window.innerWidth <= 768) {
        menuItems.forEach(item => item.classList.remove('active'));
    }
});

/**
 * Frontend Functions
 */
function toggleMenu() {
    const menuBar = document.querySelector('.menu-bar');
    menuBar.style.display = menuBar.style.display === 'flex' ? 'none' : 'flex';
}

function showRequestsScreen() {
    var contentSection1 = document.getElementById('newRequest');
    var contentSection2 = document.getElementById('historyR');
    var contentSection3 = document.getElementById('offerG');
    var contentSection4 = document.getElementById('offerGH');

    contentSection1.style.display = 'block';
    contentSection2.style.display = 'block';
    contentSection3.style.display = 'none';
    contentSection4.style.display = 'none';

    allItemCategories.then(categories => {
        populateRequestCategories(categories);
    });

    requestsData.then(requests => {
        populateRequestHistory(requests);
    });

}

function showOffersScreen() {
    var contentSection1 = document.getElementById('newRequest');
    var contentSection2 = document.getElementById('historyR');
    var contentSection3 = document.getElementById('offerG');
    var contentSection4 = document.getElementById('offerGH');

    contentSection1.style.display = 'none';
    contentSection2.style.display = 'none';
    contentSection3.style.display = 'block';
    contentSection4.style.display = 'block';

    offersData.then(offers => {
        populateOfferHistory(offers);
    });

    announcementsData.then(announcements => {
        populateNewOffer(announcements);
    });
}

function populateRequestCategories(data) {
    newRequestElement.querySelector('#searchStock').value = ''; //empty selected item


    categoryList.innerHTML = `
            <option value="" disabled selected>Επιλέξτε κατηγορία</option>
            <option value="all">All</option>
                `;
    data.forEach(row => {

        const category = row.CategoryName;
        const id = row.CategoryID;

        let categoryOption = document.createElement('option');
        categoryOption.innerHTML = category;
        categoryOption.setAttribute('value', id);
        categoryList.appendChild(categoryOption);

    });
}

function populateRequestItems(data) {
    const newRequestTable = document.getElementById('newRequest');
    const categoryList = newRequestTable.querySelector('#category');
    const itemsList = newRequestTable.querySelector('#itemsList');
    const selectedCategory = categoryList.value;

    itemsList.innerHTML = '';

    if (selectedCategory === 'all') {
        data.forEach(item => {
            let option = document.createElement('option');
            option.value = item.Name;
            itemsList.appendChild(option);
        });
    } else {
        const filteredItems = data.filter(item => item.CategoryID === selectedCategory);
        filteredItems.forEach(item => {
            let option = document.createElement('option');
            option.value = item.Name;
            itemsList.appendChild(option);
        });
    }
}

function populateRequestHistory(data) {
    const tableBody = document.querySelector('#dataTable tbody');
    tableBody.innerHTML = '';

    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="display: none;">${row.RequestID}</td> <!-- Hidden Request ID -->
            <td>${row.Name}</td>
            <td>${row.CategoryName}</td>
            <td>${row.Quantity}</td>
            <td>${row.DateCreated}</td>
            <td>${row.DateAssignedVehicle}</td> 
            <td>${row.DateFinished}</td>
            <td><input type="checkbox" class="task-checkbox" data-id="${row.Name}" 
                ${row.DateAssignedVehicle !== '-' ? 'disabled' : ''}></td> 
        `;
        tableBody.appendChild(tr);
    });
}

function populateNewOffer(data) {
    const tableBody = document.querySelector('#newDataTable tbody');
    tableBody.innerHTML = '';

    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.AnnouncementID}</td>
            <td>${row.CategoryName}</td>
            <td>${row.Name}</td>
            <td>${row.Quantity}</td>
            <td>${row.DateCreated}</td>
            <td><input type="checkbox" class="task-checkbox" data-id="${row.Name}"></td> 
        `;//todo: change to ids?
        tableBody.appendChild(tr);
    });
}

function populateOfferHistory(data) {
    const tableBody = document.querySelector('#dataTable2 tbody');
    tableBody.innerHTML = '';

    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="display: none;">${row.OfferID}</td> <!-- Hidden Offer ID -->
            <td>${row.Name}</td>
            <td>${row.CategoryName}</td>
            <td>${row.Quantity}</td>
            <td>${row.DateCreated}</td>
            <td>${row.DateAssignedVehicle}</td> 
            <td>${row.DateFinished}</td> 
            <td><input type="checkbox" class="task-checkbox" data-id="${row.Name}" 
                ${row.DateAssignedVehicle !== '-' ? 'disabled' : ''}></td> 
        `;
        tableBody.appendChild(tr);
    });
}

/**
 * Backend Functions
 */
function fetchAllExpired() {
    if (expiryDates['Requests'] == null || Date.now() - expiryDates['Requests'] > expiryTime) {
        requestsData = fetchRequests();
    }

    if (expiryDates['Offers'] == null || Date.now() - expiryDates['Offers'] > expiryTime) {
        offersData = fetchOffers();
    }

    if (expiryDates['Announcements'] == null || Date.now() - expiryDates['Announcements'] > expiryTime) {
        announcementsData = fetchAnnouncements();
    }

    if (expiryDates['Categories'] == null || Date.now() - expiryDates['Categories'] > expiryTime) {
        allItemCategories = fetchCategories();
    }

    if (expiryDates['Items'] == null || Date.now() - expiryDates['Items'] > expiryTime) {
        allItems = fetchItems();
    }
}

function fetchCategories() {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '../fetch_categories.php/', true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
                expiryDates['Categories'] = Date.now();
            } else {
                console.error('Failed to fetch all categories data');
                resolve([]);
            }
        };

        xhr.onerror = function () {
            console.error('Request error fetching categories');
            resolve([]);
        };


        xhr.send();
    });
}

function fetchItems() {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '../fetch_items.php', true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
                expiryDates['Items'] = Date.now();
            } else {
                console.error('Failed to fetch all items data');
                resolve([]);
            }
        };

        xhr.onerror = function () {
            console.error('Request error fetching items');
            resolve([]);
        };

        xhr.send();
    });
}

function fetchRequests() {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        let citizen_id = localStorage.getItem('citizen_id');
        xhr.open('GET', 'api/fetch_requests.php/' + citizen_id, true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
                expiryDates['Requests'] = Date.now();
            } else {
                console.error('Failed to fetch requests data');
                resolve([]);
            }
        };

        xhr.onerror = function () {
            console.error('Request error fetching requests');
            resolve([]);
        };

        xhr.send();
    });
};

function fetchOffers() {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        let citizen_id = localStorage.getItem('citizen_id');
        xhr.open('GET', 'api/fetch_offers.php/' + citizen_id, true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
                expiryDates['Offers'] = Date.now();
            } else {
                console.error('Failed to fetch offers data');
                resolve([]);
            }
        };

        xhr.onerror = function () {
            console.error('Request error fetching offers');
            resolve([]);
        };

        xhr.send();
    });
};

function fetchAnnouncements() {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '../fetch_announcements_detailed.php', true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
                expiryDates['Announcements'] = Date.now();
            } else {
                console.error('Failed to fetch announcements data');
                resolve([]);
            }
        };

        xhr.onerror = function () {
            console.error('Request error fetching announcements');
            resolve([]);
        };

        xhr.send();
    });
}

function createRequest(items, numOfPeople) {

    const xhr = new XMLHttpRequest();
    var citizen_id = localStorage.getItem('citizen_id');
    xhr.open('POST', 'api/create_request.php/' + citizen_id, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Define what happens when the server responds
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
                alert('Το αίτημα δημιουργήθηκε επιτυχώς!');

                requestsData = fetchRequests();
                requestsData.then(requests => {
                    populateRequestHistory(requests);
                });
            } else {
                alert('Σφάλμα: ' + response.message);
            }
        } else {
            alert('Η αίτηση απέτυχε. Κωδικός σφάλματος: ' + xhr.status);
        }
    };

    const data = `items=${encodeURIComponent(items)}
        &people=${encodeURIComponent(numOfPeople)}
    `;
    xhr.send(data);

}

function createOffer(items, quantities) {
    // Check if arrays are empty
    if (items.length === 0 || quantities.length === 0) {
        alert('Δεν έχετε επιλέξει κανένα αντικείμενο!');
        return;
    }

    const xhr = new XMLHttpRequest();
    var citizen_id = localStorage.getItem('citizen_id');
    xhr.open('POST', 'api/create_offer.php/' + citizen_id, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Define what happens when the server responds
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
                alert('Η προσφορά δημιουργήθηκε επιτυχώς!');

                offersData = fetchOffers();
                offersData.then(offers => {
                    populateOfferHistory(offers);
                });
            } else {
                alert('Σφάλμα: ' + response.message);
            }
        } else {
            alert('Η αίτηση απέτυχε. Κωδικός σφάλματος: ' + xhr.status);
        }
    };

    const data = `items=${encodeURIComponent(items)}
        &quantities=${encodeURIComponent(quantities)}
    `;
    xhr.send(data);

}

/**
 * Setup
 */
// session cookie
checkSession();  // Initial check
setInterval(checkSession, 60000);  // Check every 1 minute

document.addEventListener("DOMContentLoaded", function () {
    fetchAllExpired();
    setInterval(fetchAllExpired, expiryTime / 10); //check every 1th of the expiry time

});


// Add event listener for the delete (cancel) button using the ID
const deleteOfferButton = document.getElementById('btn_delete');
deleteOfferButton.addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default form submission behavior

    // Find selected offers (checkbox checked)
    const selectedOffers = Array.from(document.querySelectorAll('#dataTable2 input[type=checkbox]'))
        .filter(input => input.checked);

    // Ensure at least one offer is selected
    if (selectedOffers.length === 0) {
        alert('Please select an offer to cancel.');
        return;
    }

    // Get the offer IDs from the selected rows
    const selectedOfferIDs = selectedOffers.map(checkbox => {
        const row = checkbox.closest('tr');
        return row.querySelectorAll('td')[0].textContent; // Assuming the first column contains the offer ID
    });

    // Call the deleteOffer function with the selected offer IDs
    deleteOffers(selectedOfferIDs);
});

function deleteOffers(offerIDs) {
    // Check if offerIDs array is not empty
    if (offerIDs.length === 0) {
        alert('No offers selected.');
        return;
    }

    // Confirm deletion with the user
    if (!confirm('Are you sure you want to cancel the selected offer(s)?')) {
        return;
    }

    // Prepare the request
    const xhr = new XMLHttpRequest();
    var citizen_id = localStorage.getItem('citizen_id');
    xhr.open('POST', 'api/delete_offer.php/' + citizen_id, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Define what happens on server response
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
                alert('Offer(s) canceled successfully!');
                // Refresh the offer history
                offersData = fetchOffers();
                offersData.then(offers => {
                    populateOfferHistory(offers);
                });
            } else {
                alert('Error: ' + response.message);
            }
        } else {
            alert('Request failed. Error code: ' + xhr.status);
        }
    };

    // Send request with the selected offer IDs
    const data = `offerIDs=${encodeURIComponent(offerIDs.join(','))}`;
    xhr.send(data);
}

// Add event listener for the delete (cancel) button using the ID
const deleteRequestButton = document.getElementById('btn_delete_req');
deleteRequestButton.addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default form submission behavior

    // Find selected requests (checkbox checked)
    const selectedRequests = Array.from(document.querySelectorAll('#dataTable input[type=checkbox]'))
        .filter(input => input.checked);

    // Ensure at least one request is selected
    if (selectedRequests.length === 0) {
        alert('Please select a request to cancel.');
        return;
    }

    // Get the request IDs from the selected rows
    const selectedRequestIDs = selectedRequests.map(checkbox => {
        const row = checkbox.closest('tr');
        return row.querySelectorAll('td')[0].textContent; // Assuming the first column contains the offer ID
    });

    // Call the deleteRequest function with the selected offer IDs
    deleteRequests(selectedRequestIDs);
});

function deleteRequests(requestIDs) {
    // Check if offerIDs array is not empty
    if (requestIDs.length === 0) {
        alert('No requests selected.');
        return;
    }

    // Confirm deletion with the user
    if (!confirm('Are you sure you want to cancel the selected request(s)?')) {
        return;
    }

    // Prepare the request
    const xhr = new XMLHttpRequest();
    var citizen_id = localStorage.getItem('citizen_id');
    xhr.open('POST', 'api/delete_request.php/' + citizen_id, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Define what happens on server response
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
                alert('Request(s) canceled successfully!');
                // Refresh the offer history
                requestsData = fetchOffers();
                requestsData.then(requests => {
                    populateRequestHistory(requests);
                });
            } else {
                alert('Error: ' + response.message);
            }
        } else {
            alert('Request failed. Error code: ' + xhr.status);
        }
    };

    // Send request with the selected offer IDs
    const data = `requestIDs=${encodeURIComponent(requestIDs.join(','))}`;
    xhr.send(data);
}
