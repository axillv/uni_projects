// Initialize the map at a default position; this will be updated once the base location is fetched
var map = L.map('map').setView([51.505, -0.09], 16);

// Add a tile layer from OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 25,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Global variables to track markers, lines, and fil

var baseMarker; // To store the base marker
var newBaseLatLng; // To store the new coordinates after dragging
let vehicleMarkers = {}; // To store vehicle locations
let allMarkers = []; // Array to store all markers
let inProgressRequestMarkers = []; // Array to store in-progress request markers
let pendingRequestMarkers = []; // Array to store pending request markers
let offerMarkers = []; // Array to store offer markers
let activeVehicleMarkers = []; // Array to store active vehicle markers
let inactiveVehicleMarkers = []; // Array to store inactive vehicle markers
let drawnLines = []; // Array to store drawn lines

let isInProgressFilterActive = false; // State to track if the in-progress filter is active
let isPendingFilterActive = false; // State to track if the pending filter is active
let isOfferFilterActive = false; // State to track if the offer filter is active
let isActiveVehiclesFilterActive = false; // State to track if the active vehicles filter is active
let isInactiveVehiclesFilterActive = false; // State to track if the inactive vehicles filter is active
let isLinesFilterActive = false; // State to track if the lines filter is active

let initialLoad = true; // Flag to check if it's the first load

// Custom icons for different statuses and types
var baseIcon = L.icon({
    iconUrl: '../markers/base.svg',  // Path to your custom icon
    iconSize: [35, 50],
    iconAnchor: [15, 45],
    popupAnchor: [0, -45],
});

var pendingRequestIcon = L.icon({
    iconUrl: '../markers/pendingRequestIcon_red.svg',
    iconSize: [35, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});

var inProgressRequestIcon = L.icon({
    iconUrl: '../markers/inProgressRequestIcon_green.svg',
    iconSize: [35, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});

var pendingOfferIcon = L.icon({
    iconUrl: '../markers/pendingOfferIcon_orange.svg', // Replace with your icon path
    iconSize: [35, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],

});

var inProgressOfferIcon = L.icon({
    iconUrl: '../markers/inProgressOfferIcon_blue.svg', // Replace with your icon path
    iconSize: [35, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});

// Create a custom icon for the vehicle marker
var blueIcon = new L.Icon({
    iconUrl: '../markers/vehicle.svg', // Replace with your icon path
    iconSize: [35, 50],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
});

let currentCenter; // To store the current center of the map
let currentZoom;  // To store the current zoom level of the map

function fetchDataAndUpdateMap() {

    // Save the current center and zoom level before fetching the data
    if (!initialLoad) {
        currentCenter = map.getCenter();
        currentZoom = map.getZoom();
    }

    fetch('map_fetch.php')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }
            updateMap(data);
          // On initial load, show all vehicles by default
          if (initialLoad) {
            showAllVehicles(); // Add both active and inactive vehicles to the map
            initialLoad = false; // Ensure this only happens on the first load
        }

            // After updating the map, reapply the vehicle filters based on the current states
            applyVehicleFilters();
        })
        .catch(error => {
            console.error('Fetch Error:', error);
        });
}

// Helper function to reapply filters based on the active states
function applyVehicleFilters() {
    // Reapply the "active vehicles" filter if it's currently active
    if (!isActiveVehiclesFilterActive) {
        activeVehicleMarkers.forEach(marker => marker.addTo(map));
    } else {
        activeVehicleMarkers.forEach(marker => map.removeLayer(marker));
    }

    // Reapply the "inactive vehicles" filter if it's currently active
    if (!isInactiveVehiclesFilterActive) {
        inactiveVehicleMarkers.forEach(marker => marker.addTo(map));
    } else {
        inactiveVehicleMarkers.forEach(marker => map.removeLayer(marker));
    }
}



// Function to clear all lines from the map
function clearLines() {
    drawnLines.forEach(line => map.removeLayer(line));
    drawnLines = [];
}


// Function to draw lines between vehicle and tasks
function drawLines(vehicle, requests, offers) {
    clearLines();

    // Draw lines to assigned requests
    if (vehicle.AssignedRequests) {
        vehicle.AssignedRequests.split(',').forEach(reqID => {
            const request = requests.find(r => r.RequestID == reqID);
            if (request) {
                const line = L.polyline([[vehicle.VehicleLat, vehicle.VehicleLng], [request.RequestLat, request.RequestLng]], {
                    color: 'green'
                }).addTo(map);
                drawnLines.push(line);
            }
        });
    }

    // Draw lines to assigned offers
    if (vehicle.AssignedOffers) {
        vehicle.AssignedOffers.split(',').forEach(offerID => {
            const offer = offers.find(o => o.OfferID == offerID);
            if (offer) {
                const line = L.polyline([[vehicle.VehicleLat, vehicle.VehicleLng], [offer.OfferLat, offer.OfferLng]], {
                    color: 'blue'
                }).addTo(map);
                drawnLines.push(line);
            }
        });
    }
}


// Function to draw a line between a request/offer and its assigned vehicle using VehicleID
function drawLineToAssignedVehicle(marker, assignedVehicleID, vehicleMarkers) {
    clearLines(); // Clear existing lines

    const vehicleLatLng = vehicleMarkers[assignedVehicleID];
    if (vehicleLatLng) {
        const line = L.polyline([[marker.getLatLng().lat, marker.getLatLng().lng], [vehicleLatLng.lat, vehicleLatLng.lng]], {
            color: 'green'
        }).addTo(map);
        drawnLines.push(line);
    }
}


// Function to update the map with base, vehicle, offer, and request data
function updateMap(mapData) {
    const base = mapData.base;
    

    // Clear previous markers and lines
    allMarkers.forEach(marker => map.removeLayer(marker));
    inProgressRequestMarkers.forEach(marker => map.removeLayer(marker));
    pendingRequestMarkers.forEach(marker => map.removeLayer(marker));
    offerMarkers.forEach(marker => map.removeLayer(marker));
    activeVehicleMarkers.forEach(marker => map.removeLayer(marker));
    inactiveVehicleMarkers.forEach(marker => map.removeLayer(marker));
    drawnLines.forEach(line => map.removeLayer(line));
    
    allMarkers = []; // Reset the marker arrays
    inProgressRequestMarkers = [];
    pendingRequestMarkers = [];
    offerMarkers = [];
    activeVehicleMarkers = [];
    inactiveVehicleMarkers = [];
    drawnLines = [];

    // Clear the base marker if it exists
    if (baseMarker) {
        map.removeLayer(baseMarker);
    }

    // Add the base marker with the custom icon
    baseMarker = L.marker([base.Latitude, base.Longitude], { icon: baseIcon, draggable: true })
        .addTo(map)
        .bindPopup(`<b>${base.BaseName}</b><br>Drag to change location.`)
        .openPopup();

    // Handle dragging of the base marker
    baseMarker.on('dragend', function (event) {
        newBaseLatLng = event.target.getLatLng();
        showConfirmPopup(); // Show confirmation popup when dragging ends
    });

    // If it's the initial load (browser refresh), set the map to the base location
    if (initialLoad) {
        map.setView([base.Latitude, base.Longitude], 16);
        initialLoad = false; // Reset the flag after the initial load
    } else {
        // Reapply the saved center and zoom level after the update
        if (currentCenter && currentZoom) {
            map.setView(currentCenter, currentZoom);
        }
    }


    // Store vehicle locations for easy lookup
    mapData.vehicles.forEach(function (vehicle) {
        vehicleMarkers[vehicle.VehicleID] = { lat: vehicle.VehicleLat, lng: vehicle.VehicleLng };

        // Determine if the vehicle is active or inactive
        let vehicleMarker = L.marker([vehicle.VehicleLat, vehicle.VehicleLng], { icon: blueIcon });

        if (vehicle.ActiveTasks > 0) {
            activeVehicleMarkers.push(vehicleMarker);
        } else {
            inactiveVehicleMarkers.push(vehicleMarker);
        }

        // If both active and inactive filters are disabled, show all vehicles
        if (!isActiveVehiclesFilterActive && !isInactiveVehiclesFilterActive) {
            vehicleMarker.addTo(map);
        } 
        // If only active vehicles filter is enabled, show vehicles with active tasks
        else if (isActiveVehiclesFilterActive && vehicle.ActiveTasks > 0) {
            vehicleMarker.addTo(map);
        } 
        // If only inactive vehicles filter is enabled, show vehicles without active tasks
        else if (isInactiveVehiclesFilterActive && vehicle.ActiveTasks === 0) {
            vehicleMarker.addTo(map);
        }


        vehicleMarker.on('click', function () {
            clearLines(); // Clear lines when clicking a new marker
            showPopup({
                type: "vehicle-box",
                title: "Όχημα",
                details: `
                <p><strong>Διακριτικό Οχήματος:</strong> ${vehicle.RescuerUsername}</p>
                <p><strong>Φορτίο:</strong> ${vehicle.Load}</p>
                <p><strong>Κατάσταση:</strong> ${vehicle.Status}</p>
                <p><strong>Ενεργά Tasks:</strong> ${vehicle.ActiveTasks > 0 ? 'Ναι' : 'Όχι'}</p>
            `
            });

            // Draw lines only if the lines filter is not active
            if (!isLinesFilterActive) {
                drawLines(vehicle, mapData.requests, mapData.offers);
            }
        });
    });

    // Add request markers
    mapData.requests.forEach(function (request) {
        var icon = request.Status === 'PENDING' ? pendingRequestIcon : inProgressRequestIcon;
        var requestMarker = L.marker([request.RequestLat, request.RequestLng], { icon: icon });

        // Add to the respective arrays
        allMarkers.push(requestMarker);
        if (request.Status === 'INPROGRESS') {
            inProgressRequestMarkers.push(requestMarker);
        } else if (request.Status === 'PENDING') {
            pendingRequestMarkers.push(requestMarker);
        }

        // Add marker to the map if the filters are not active or if it should be displayed
        if ((!isInProgressFilterActive || request.Status !== 'INPROGRESS') &&
            (!isPendingFilterActive || request.Status !== 'PENDING')) {
            requestMarker.addTo(map);
        }

        requestMarker.on('click', function () {
            clearLines(); // Clear lines when clicking a new marker
            showPopup({
                type: "request-box",
                title: "Αίτημα",
                details: `
                <p><strong>Ονοματεπώνυμο:</strong> ${request.Name}</p>
                <p><strong>Τηλέφωνο:</strong> ${request.Phone}</p>
                <p><strong>Ημ/νια Καταχώρησης:</strong> ${request.DateCreated}</p>
                <p><strong>Είδη:</strong> ${request.ItemNames}</p>
                <p><strong>Ποσότητες:</strong> ${request.ItemQuantities}</p>
                ${request.RescuerUsername ? `<p><strong>Ημ/νια Ανάληψης Οχήματος:</strong> ${request.DateAssignedVehicle}</p>` : ''}
                ${request.RescuerUsername ? `<p><strong>Αναλήφθηκε από:</strong> ${request.RescuerUsername}</p>` : ''}
            `
            });

            // Draw a line to the assigned vehicle if in progress
            if (request.Status === 'INPROGRESS' && request.AssignedVehicleID && !isLinesFilterActive) {
                drawLineToAssignedVehicle(requestMarker, request.AssignedVehicleID, vehicleMarkers);
            }
        });
    });

    // Add offer markers
    mapData.offers.forEach(function (offer) {
        var icon = offer.Status === 'PENDING' ? pendingOfferIcon : inProgressOfferIcon;
        var offerMarker = L.marker([offer.OfferLat, offer.OfferLng], { icon: icon });

        // Add to the respective array
        allMarkers.push(offerMarker);
        offerMarkers.push(offerMarker);

        // Add marker to the map if the filter is not active
        if (!isOfferFilterActive) {
            offerMarker.addTo(map);
        }

        offerMarker.on('click', function () {
            clearLines(); // Clear lines when clicking a new marker
            showPopup({
                type: "offer-box",
                title: "Προσφορά",
                details: `
                <p><strong>Ονοματεπώνυμο:</strong> ${offer.Name}</p>
                <p><strong>Τηλέφωνο:</strong> ${offer.Phone}</p>
                <p><strong>Ημ/νια Καταχώρησης:</strong> ${offer.DateCreated}</p>
                <p><strong>Είδη:</strong> ${offer.ItemNames}</p>
                <p><strong>Ποσότητες:</strong> ${offer.ItemQuantities}</p>
                ${offer.DateAssignedVehicle ? `<p><strong>Ημ/νια Ανάληψης Οχήματος:</strong> ${offer.DateAssignedVehicle}</p>` : ''}
                ${offer.RescuerUsername ? `<p><strong>Αναλήφθηκε από:</strong> ${offer.RescuerUsername}</p>` : ''}
            `
            });

            // Draw a line to the assigned vehicle if in progress
            if (offer.Status === 'INPROGRESS' && offer.AssignedVehicleID && !isLinesFilterActive) {
                drawLineToAssignedVehicle(offerMarker, offer.AssignedVehicleID, vehicleMarkers);
            }
        });
    });

}

// Function to toggle the filter for "Taken Requests"
function toggleInProgressRequests() {
    const button = document.getElementById('toggleTakenRequests');
    
    if (isInProgressFilterActive) {
        inProgressRequestMarkers.forEach(marker => marker.addTo(map)); // Re-add in-progress markers
        button.classList.remove('active-filter');
    } else {
        inProgressRequestMarkers.forEach(marker => map.removeLayer(marker)); // Remove in-progress markers
        button.classList.add('active-filter');
    }
    
    isInProgressFilterActive = !isInProgressFilterActive;
}

// Function to toggle the filter for "Pending Requests"
function togglePendingRequests() {
    const button = document.getElementById('togglePendingRequests');
    
    if (isPendingFilterActive) {
        pendingRequestMarkers.forEach(marker => marker.addTo(map)); // Re-add pending markers
        button.classList.remove('active-filter');
    } else {
        pendingRequestMarkers.forEach(marker => map.removeLayer(marker)); // Remove pending markers
        button.classList.add('active-filter');
    }
    
    isPendingFilterActive = !isPendingFilterActive;
}

// Function to toggle the filter for "Offers"
function toggleOffers() {
    const button = document.getElementById('toggleOffers');
    
    if (isOfferFilterActive) {
        offerMarkers.forEach(marker => marker.addTo(map)); // Re-add offer markers
        button.classList.remove('active-filter');
    } else {
        offerMarkers.forEach(marker => map.removeLayer(marker)); // Remove offer markers
        button.classList.add('active-filter');
    }
    
    isOfferFilterActive = !isOfferFilterActive;
}

// Function to toggle the filter for "Active Vehicles"
function toggleActiveVehicles() {
    const button = document.getElementById('toggleActiveVehicles');
    
    if (!isActiveVehiclesFilterActive) {
        activeVehicleMarkers.forEach(marker => map.removeLayer(marker)); // Hide active vehicles
        button.classList.add('active-filter'); // Mark button as active
    } else {
        activeVehicleMarkers.forEach(marker => marker.addTo(map)); // Show active vehicles
        button.classList.remove('active-filter'); // Mark button as inactive
    }

    isActiveVehiclesFilterActive = !isActiveVehiclesFilterActive; // Toggle state
}

// Function to toggle the filter for "Inactive Vehicles"
function toggleInactiveVehicles() {
    const button = document.getElementById('toggleInactiveVehicles');
    
    if (!isInactiveVehiclesFilterActive) {
        inactiveVehicleMarkers.forEach(marker => map.removeLayer(marker)); // Hide inactive vehicles
        button.classList.add('active-filter'); // Mark button as active
    } else {
        inactiveVehicleMarkers.forEach(marker => marker.addTo(map)); // Show inactive vehicles
        button.classList.remove('active-filter'); // Mark button as inactive
    }

    isInactiveVehiclesFilterActive = !isInactiveVehiclesFilterActive; // Toggle state
}


// Function to toggle the filter for "Lines"
function toggleLines() {
    const button = document.getElementById('toggleLines');
    
    if (isLinesFilterActive) {
        drawnLines.forEach(line => line.addTo(map)); // Re-add lines
        button.classList.remove('active-filter');
    } else {
        drawnLines.forEach(line => map.removeLayer(line)); // Remove lines
        button.classList.add('active-filter');
    }
    
    isLinesFilterActive = !isLinesFilterActive;
}

// Add event listeners for the toggle buttons
document.getElementById('toggleTakenRequests').addEventListener('click', toggleInProgressRequests);
document.getElementById('togglePendingRequests').addEventListener('click', togglePendingRequests);
document.getElementById('toggleOffers').addEventListener('click', toggleOffers);
document.getElementById('toggleActiveVehicles').addEventListener('click', toggleActiveVehicles);
document.getElementById('toggleInactiveVehicles').addEventListener('click', toggleInactiveVehicles);
document.getElementById('toggleLines').addEventListener('click', toggleLines);


// Function to show the confirmation popup
function showConfirmPopup() {
    const confirmationBox = document.getElementById('confirmationBox');
    confirmationBox.style.display = 'block';
}

// Function to confirm the new base location
function confirmBaseLocation() {
    if (newBaseLatLng) {
        // Send new base location to the server using Fetch API
        fetch('update_base_location.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                latitude: newBaseLatLng.lat,
                longitude: newBaseLatLng.lng
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Base location updated successfully!');
                const confirmationBox = document.getElementById('confirmationBox');
                confirmationBox.style.display = 'none';
            } else {
                alert('Failed to update base location. ' + (data.error ? data.error : ''));
            }
        })
        .catch(error => {
            alert('Failed to send data to the server. Error: ' + error.message);
        });
    }
}


// Function to cancel the base location update
function cancelBaseLocation() {
    const confirmationBox = document.getElementById('confirmationBox');
    confirmationBox.style.display = 'none';
    newBaseLatLng = null; // Reset the new location
}

// Function to show the vehicle popup
function showPopup({ type, title, details }) {
    const popup = document.getElementById('draggableBox');
    popup.className = type;
    const popupTitle = popup.querySelector('.offer-title');
    const popupDetails = popup.querySelector('.offer-details');

    popupTitle.innerHTML = title;
    popupDetails.innerHTML = details;

    popup.style.display = 'flex';
}

// Close button event for vehicle popup
document.getElementById('closeBox').addEventListener('click', function () {
    document.getElementById('draggableBox').style.display = 'none';
    clearLines();
});

// Confirm button event for base location
document.getElementById('confirmButton').addEventListener('click', confirmBaseLocation);

// Cancel button event for base location
document.getElementById('cancelButton').addEventListener('click', cancelBaseLocation);


// Initial fetch and update of the map
fetchDataAndUpdateMap();

// Fetch and update map data every 10 seconds
setInterval(fetchDataAndUpdateMap, 10000);

// Get the popup element and close button
var externalPopup = document.getElementById('draggableBox');
var closePopup = document.getElementById('closeBox');




