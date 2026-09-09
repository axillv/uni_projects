// Function to fetch items from the server and populate only the original select element
function fetchAndPopulateItems() {
    fetch('get_items.php')
        .then(response => response.json())
        .then(items => {
            // Populate the main type dropdown
            const typeSelect = document.getElementById('type');
            typeSelect.innerHTML = ''; // Clear existing options

            // Add default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.disabled = true;
            defaultOption.selected = true;
            defaultOption.textContent = 'Επιλέξτε είδος';
            typeSelect.appendChild(defaultOption);

            // Populate options with items fetched from the server
            items.forEach(item => {
                const option = document.createElement('option');
                option.value = item.Name; // Use the item Name as the value
                option.textContent = item.Name; // Use the item Name as the display text
                typeSelect.appendChild(option);
            });

            // Store fetched items globally for use in dynamic fields
            document.currentItems = items;
        })
        .catch(error => {
            console.error('Error fetching items:', error);
        });
}

// Function to dynamically add new sets of fields
function addDynamicFields() {
    const additionalFields = document.getElementById('additionalFields');
    const extraRequests = document.getElementById('extraRequests').value;
    const extraCount = parseInt(extraRequests);

    // Clear previous fields
    additionalFields.innerHTML = '';

    // Validate the input
    if (isNaN(extraCount) || extraCount < 1) {
        alert("Please enter a valid number of extra requests.");
        return;
    }

    // Add new sets of fields based on the number entered
    for (let i = 1; i <= extraCount; i++) {
        // Create label and dropdown for item type
        const typeLabel = document.createElement("label");
        typeLabel.textContent = "Είδος " + i;
        const typeSelect = document.createElement("select");
        typeSelect.name = "extraType" + i;

        // Populate the select dropdown with the available items
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        defaultOption.textContent = 'Επιλέξτε είδος';
        typeSelect.appendChild(defaultOption);

        // Use the globally stored items to populate each new dropdown
        document.currentItems.forEach(item => {
            const option = document.createElement('option');
            option.value = item.Name;
            option.textContent = item.Name;
            typeSelect.appendChild(option);
        });

        // Create label and input for quantity
        const quantityLabel = document.createElement("label");
        quantityLabel.textContent = "Ποσότητα " + i;
        const quantityInput = document.createElement("input");
        quantityInput.type = "text";
        quantityInput.name = "extraQuantity" + i;
        quantityInput.placeholder = "Ποσότητα";

        // Append the new fields to the form
        additionalFields.appendChild(typeLabel);
        additionalFields.appendChild(typeSelect);
        additionalFields.appendChild(quantityLabel);
        additionalFields.appendChild(quantityInput);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    fetchAndPopulateItems(); // Populate the original dropdown when the page loads

    const addButton = document.querySelector(".btn.add-fields");
    addButton.addEventListener('click', addDynamicFields); // Add fields when button is clicked

    const submitButton = document.getElementById('anasub');
    submitButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the form from submitting normally

        const type = document.getElementById('type').value;
        const quantity = document.getElementById('quantity').value;

        // Collect the main item and quantity
        const items = [{ name: type, quantity: parseInt(quantity) }];

        // Collect extra items and quantities from dynamic fields
        const extraFields = document.getElementById('additionalFields').children;
        for (let i = 0; i < extraFields.length; i += 4) {
            const extraType = extraFields[i + 1].value;
            const extraQuantity = extraFields[i + 3].value;
            if (extraType && extraQuantity) {
                items.push({ name: extraType, quantity: parseInt(extraQuantity) });
            }
        }

        // Get admin ID from localStorage (set during login)
        const adminID = localStorage.getItem('admin_id'); 
        if (!adminID) {
            alert('Admin ID not found. Please log in again.');
            return;
        }

        // Send the data to the server via AJAX
        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'createannouncement.php', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                    alert('Η ανακοίνωση δημιουργήθηκε επιτυχώς!');
                    document.getElementById('newAithmata').reset(); // Clear the form fields
                    document.getElementById('additionalFields').innerHTML = ''; // Clear additional fields
                } else {
                    alert('Σφάλμα: ' + response.message);
                }
            } else {
                alert('Η αίτηση απέτυχε. Κωδικός σφάλματος: ' + xhr.status);
            }
        };

        // Prepare the data to be sent to the server
        const data = JSON.stringify({ adminID: adminID, items: items });
        xhr.send(data);
    });
});