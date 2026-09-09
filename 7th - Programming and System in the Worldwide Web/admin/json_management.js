document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileUpload');
    const urlInput = document.getElementById('simpleText'); // URL input for JSON
    const dropArea = document.getElementById('dropArea');

    // Handling file selection via click
    dropArea.addEventListener('click', () => {
        fileInput.click(); // Trigger file input click on drop area click
    });

    // Handle file selection via file dialog
    fileInput.addEventListener('change', () => {
        const files = fileInput.files;
        if (files.length && files[0].type === 'application/json') {
            processFile(files[0]); // Call function to handle file upload
        } else {
            alert('Please select a valid JSON file.');
            fileInput.value = ''; // Clear the input if invalid file type is selected
        }
    });

    // Function to process the selected file
    function processFile(jsonFile) {
        const reader = new FileReader();
        reader.onload = function (event) {
            try {
                const data = JSON.parse(event.target.result);
                sendJsonToServer(data, 'json_management.php'); // Send data to the file upload PHP
            } catch (error) {
                alert('Invalid JSON file.');
            }
        };
        reader.readAsText(jsonFile); // Read the uploaded file as text
        fileInput.value = ''; // Reset the file input after upload
    }

    // Submit button action for fetching JSON from URL
    document.getElementById('submitTextFieldForm').addEventListener('click', function () {
        const url = urlInput.value.trim();
        if (url) {
            fetchJsonFromUrl(url); // Call function to handle URL-based JSON fetching
        } else {
            alert('Please enter a valid URL.');
        }
    });

    // Function to fetch JSON data from URL
    function fetchJsonFromUrl(url) {
        fetch('load_url_items.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }) // Send the URL to the server
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Data successfully inserted into the database.');
            } else {
                alert('Error inserting data: ' + data.message);
            }
        })
        .catch(error => alert('Error fetching data from the URL: ' + error.message));
    }

    // Function to send JSON data to the server (for both file and URL)
    function sendJsonToServer(jsonData, phpEndpoint) {
        fetch(phpEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'processJson', data: jsonData }) // Send the JSON data
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Data successfully inserted into the database.');
            } else {
                alert('Error inserting data: ' + data.message);
            }
        })
        .catch(error => alert('Error inserting data.'));
    }
});
