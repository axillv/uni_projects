document.addEventListener('DOMContentLoaded', function () {
    const filterSelect = document.getElementById('filterType');
    const dataTableBody = document.querySelector('#dataTable tbody');
    let allItems = [];
    let selectedCategories = [];

    // Fetch data from the server
    function fetchData() {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', 'fetch_inventory.php', true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                try {
                    console.log("Raw response from the server: ", xhr.responseText); // Log the raw response
                    allItems = JSON.parse(xhr.responseText);
                    console.log("Parsed JSON data:", allItems); // Log parsed JSON data

                    if (Array.isArray(allItems) && allItems.length > 0) {
                        populateFilterOptions(allItems);
                        applyFilters(); // Apply filters after populating options
                    } else {
                        console.warn("No valid data received from server");
                        dataTableBody.innerHTML = '<tr><td colspan="6">No data available</td></tr>';
                    }
                } catch (error) {
                    console.error("Error parsing JSON data:", error);
                }
            } else {
                console.error('Failed to fetch data. Status:', xhr.status);
            }
        };

        xhr.send();
    }

    // Populate filter dropdown with unique categories
    function populateFilterOptions(items) {
        const uniqueCategories = [...new Set(items.map(item => item.Category))];
        console.log("Unique categories: ", uniqueCategories); // Log unique categories
        filterSelect.innerHTML = ''; // Clear current options

        // Add the "All" option
        const allOption = document.createElement('option');
        allOption.value = 'all';
        allOption.textContent = 'All';
        filterSelect.appendChild(allOption);

        // Add other categories
        uniqueCategories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            filterSelect.appendChild(option);
        });

        // Set "All" as the default selected option
        filterSelect.value = 'all';
        selectedCategories = ['all'];
    }

    // Apply selected filters to the items
    function applyFilters() {
        if (selectedCategories.length === 0 || selectedCategories.includes('all')) {
            renderTable(allItems); // If "All" is selected, show all items
        } else {
            const filteredItems = allItems.filter(item => selectedCategories.includes(item.Category));
            renderTable(filteredItems);
        }
    }

    // Render the items into the table
    function renderTable(items) {
        dataTableBody.innerHTML = ''; // Clear the existing table rows
        if (items.length === 0) {
            dataTableBody.innerHTML = '<tr><td colspan="6">No items found.</td></tr>';
            return;
        }

        items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.Category || 'Unknown'}</td>
                <td>${item.Name || 'Unnamed'}</td>
                <td>${item.DetailName || 'No Detail Name'}</td>
                <td>${item.DetailValue || 'No Detail Value'}</td>
                <td>${item.Location || 'Unknown' }</td>
                <td>${item.Quantity || 0}</td>
                <td>${item.ItemID}</td>
            `;
            dataTableBody.appendChild(row);
        });
    }

    // Filter change event handler
    filterSelect.addEventListener('change', function () {
        selectedCategories = Array.from(filterSelect.selectedOptions).map(option => option.value);
        applyFilters(); // Apply filters after selection
    });

    // Fetch data and populate the table initially
    fetchData();

    // Set up an interval to refresh the data every 10 seconds
    setInterval(fetchData, 10000);
});
