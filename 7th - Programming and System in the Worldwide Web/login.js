document.addEventListener('DOMContentLoaded', function() {
    // Login button functionality
    document.getElementById('loginButton').addEventListener('click', function() {
        var username = document.getElementById('usernameF').value;
        var password = document.getElementById('passwordF').value;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'login.php', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.success) {

                            // Store the specific ID (AdminID, RescuerID, CitizenID) and create session cookie
                            localStorage.setItem('role', response.role);

                            if (response.role === 'Administrator') {

                                // Set a cookie for 20 minutes (active session)
                                setCookie('admin_session', 'active', 20000);
                                // Store the admin ID in localStorage
                                localStorage.setItem('admin_id', response.specificID);
                                
                                window.location.href = 'Admin/admin.html';

                            } else if (response.role === 'Citizen') {
                                
                                //TODO: Set a cookie for 20 minutes!!!!!!!!!!!
                                setCookie('citizen_session', 'active', 20000);
                                localStorage.setItem('citizen_id', response.specificID);

                                window.location.href = 'Citizen/citizen.html';

                            }else if (response.role === 'Rescuer') {
                                
                                // Set a cookie for 20 minutes (active session)
                                setCookie('rescuer_session', 'active', 20000);
                                localStorage.setItem('rescuer_id', response.specificID);
                                
                                window.location.href = 'Rescuer/rescuer.html';

                            }else {
                                window.location.href = 'blank.html';
                            }
                        } else {
                            alert('Login failed: ' + response.message);
                        }
                    } catch (e) {
                        console.error('Error parsing JSON:', e);
                        alert('An error occurred during login.');
                    }
                } else {
                    console.log('Server returned an error status:', xhr.status);
                }
            }
        };
        
        var data = 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password);
        xhr.send(data);
    });

    // Function to set a cookie
    function setCookie(name, value, minutes) {
        var expires = "";
        if (minutes) {
            var date = new Date();
            date.setTime(date.getTime() + (minutes * 60 * 1000)); // Convert minutes to milliseconds
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    }

    // Registration pop-up toggle
    document.getElementById('registerLink').addEventListener('click', function() {
        resetRegistrationForm(); // Reset the form to the first stage
        document.getElementById('contF').classList.remove('active');
        document.getElementById('registerPopup').classList.add('active');
    });

    document.getElementById('exitRegisterButton').addEventListener('click', function() {
        document.getElementById('registerPopup').classList.remove('active');
    });

    // Next button functionality to move to second stage
    document.getElementById('nextButton').addEventListener('click', function() {
        document.getElementById('firstStage').style.display = 'none';
        document.getElementById('secondStage').style.display = 'block';
        initializeMap();
    });
    
    // Function to initialize Leaflet map
    function initializeMap() {
        var map = L.map('map').setView([37.978278, 23.727090], 13); // Default center and zoom level

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);

        var marker = L.marker([37.978278, 23.727090]).addTo(map); // Default marker location

        map.on('click', function(e) {
            var lat = e.latlng.lat;
            var lng = e.latlng.lng;
            marker.setLatLng(e.latlng); // Move marker to clicked location
            document.getElementById('latitude').value = lat;
            document.getElementById('longitude').value = lng;
        });
    }

    // Function to reset the registration form
    function resetRegistrationForm() {
        document.getElementById('firstStage').style.display = 'block';
        document.getElementById('secondStage').style.display = 'none';
        document.getElementById('registerUsername').value = '';
        document.getElementById('registerPassword').value = '';
        document.getElementById('firstName').value = '';
        document.getElementById('lastName').value = '';
        document.getElementById('phoneNumber').value = '';
        document.getElementById('latitude').value = '';
        document.getElementById('longitude').value = '';
    }

    // Register button functionality
    document.getElementById('registerButton').addEventListener('click', function() {
        var username = document.getElementById('registerUsername').value;
        var password = document.getElementById('registerPassword').value;
        var firstName = document.getElementById('firstName').value;
        var lastName = document.getElementById('lastName').value;
        var phoneNumber = document.getElementById('phoneNumber').value;
        var latitude = document.getElementById('latitude').value;
        var longitude = document.getElementById('longitude').value;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'register.php', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.success) {
                            alert('Registration successful! Please log in.');
                            document.getElementById('registerPopup').classList.remove('active');
                        } else {
                            alert('Registration failed: ' + response.message);
                        }
                    } catch (e) {
                        console.error('Error parsing JSON:', e);
                        alert('An error occurred during registration.');
                    }
                } else {
                    console.log('Server returned an error status:', xhr.status);
                }
            }
        };
        
        var data = 'username=' + encodeURIComponent(username) +
                   '&password=' + encodeURIComponent(password) +
                   '&firstName=' + encodeURIComponent(firstName) +
                   '&lastName=' + encodeURIComponent(lastName) +
                   '&phoneNumber=' + encodeURIComponent(phoneNumber) +
                   '&latitude=' + encodeURIComponent(latitude) +
                   '&longitude=' + encodeURIComponent(longitude);
        xhr.send(data);
    });
});
