document.addEventListener('DOMContentLoaded', function () {
    fetchCategories();

    // Function to fetch categories for dropdown
    function fetchCategories() {
        fetch('warehouse_management.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'action=fetchCategories'
        })
        .then(response => response.json())
        .then(data => {
            const categoryDropdown = document.getElementById('category');
            categoryDropdown.innerHTML = '<option value="" disabled selected>Επιλέξτε κατηγορία</option>';
            data.forEach(category => {
                const option = document.createElement('option');
                option.value = category.CategoryID;
                option.textContent = category.CategoryName;
                categoryDropdown.appendChild(option);
            });

            // Add the "New Category" option
            const newCategoryOption = document.createElement('option');
            newCategoryOption.value = 'newCategory';
            newCategoryOption.textContent = 'Δημιουργία νέας κατηγορίας';
            categoryDropdown.appendChild(newCategoryOption);
        })
        .catch(error => displayError('Error fetching categories.'));
    }

    // Function to display error messages
    function displayError(message) {
        alert(message); // You can also display it elsewhere in the UI if needed
    }

    // Event listener for category dropdown
    document.getElementById('category').addEventListener('change', function () {
        const categoryId = this.value;
        if (categoryId === 'newCategory') {
            const newCategoryName = prompt('Enter the new category name:');
            if (newCategoryName) {
                createCategory(newCategoryName);
            }
        } else {
            fetchItems(categoryId);
        }
    });

    // Function to fetch items for the selected category
    function fetchItems(categoryId) {
        fetch('warehouse_management.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=fetchItems&categoryId=${categoryId}`
        })
        .then(response => response.json())
        .then(data => {
            const itemDropdown = document.getElementById('item');
            itemDropdown.innerHTML = '<option value="" disabled selected>Επιλέξτε είδος ή Δημιουργία Νέου</option>';
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.ItemID;
                option.textContent = item.Name;
                itemDropdown.appendChild(option);
            });
        })
        .catch(error => displayError('Error fetching items.'));
    }

    // Function to create a new category
    function createCategory(categoryName) {
        fetch('warehouse_management.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=createCategory&categoryName=${encodeURIComponent(categoryName)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('New category created successfully!');
                fetchCategories(); // Reload categories after adding the new one
            } else {
                displayError(data.message || 'Error creating category.');
            }
        })
        .catch(error => displayError('Error creating category.'));
    }

    // Function to create a new item when Create button is clicked
    document.getElementById('CreateeButton').addEventListener('click', function () {
        const categoryId = document.getElementById('category').value;
        if (!categoryId || categoryId === 'newCategory') {
            displayError('Please select a category or create a new one.');
            return;
        }

        const itemName = prompt('Enter the new item name:');
        const detailName = document.getElementById('DetailName').value;
        const detailValue = document.getElementById('DetailValue').value;
        const quantity = document.getElementById('quantityy').value;

        if (!itemName || !detailName || !detailValue || !quantity) {
            displayError('Please fill in all fields to create a new item.');
            return;
        }

        if (isNaN(quantity) || quantity <= 0) {
            displayError('Please enter a valid positive number for the quantity.');
            return;
        }

        createItem(categoryId, itemName, detailName, detailValue, quantity);
    });

    // Function to create a new item
    function createItem(categoryId, itemName, detailName, detailValue, quantity) {
        fetch('warehouse_management.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=createItem&categoryId=${categoryId}&itemName=${encodeURIComponent(itemName)}&detailName=${encodeURIComponent(detailName)}&detailValue=${encodeURIComponent(detailValue)}&quantity=${quantity}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('New item created successfully!');
                fetchItems(categoryId); // Reload the items after adding the new one
            } else {
                displayError(data.message || 'Error creating item.');
            }
        })
        .catch(error => displayError('Error creating item probably item already exist check dropdown.'));
    }

    // Function to fetch item details when an item is selected
    document.getElementById('item').addEventListener('change', function () {
        const itemId = this.value;
        fetchItemDetails(itemId);
    });

    // Function to fetch item details
    function fetchItemDetails(itemId) {
        fetch('warehouse_management.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=fetchItemDetails&itemId=${itemId}`
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('DetailName').value = data.DetailName || '';
            document.getElementById('DetailValue').value = data.DetailValue || '';
            document.getElementById('quantityy').value = data.Quantity || 0;
        })
        .catch(error => displayError('Error fetching item details.'));
    }

    // Function to update item details
    function updateItemDetails() {
        const itemId = document.getElementById('item').value;
        const detailName = document.getElementById('DetailName').value;
        const detailValue = document.getElementById('DetailValue').value;
        const quantity = document.getElementById('quantityy').value;

        if (!itemId || !detailName || !detailValue || !quantity) {
            displayError('Please ensure all fields are filled out.');
            return;
        }

        if (isNaN(quantity) || quantity <= 0) {
            displayError('Please enter a valid positive number for the quantity.');
            return;
        }

        fetch('warehouse_management.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=updateItemDetails&itemId=${itemId}&detailName=${encodeURIComponent(detailName)}&detailValue=${encodeURIComponent(detailValue)}&quantity=${quantity}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Item details updated successfully!');
                fetchItemDetails(itemId); // Reload the updated item details
            } else {
                displayError(data.message || 'Error updating item.');
            }
        })
        .catch(error => displayError('Error updating item details.'));
    }

    // Event listener for the submit button (Υποβολή)
    document.getElementById('submitButton').addEventListener('click', function () {
        updateItemDetails();
    });

    // Automatically refresh item details every 30 seconds
    setInterval(function () {
        const itemId = document.getElementById('item').value;
        if (itemId) {
            fetchItemDetails(itemId);
        }
    }, 30000); // 30 seconds interval

    // Delete buttons for category and item
    const categoryDeleteButton = document.createElement('button');
    categoryDeleteButton.textContent = '🗑️';
    categoryDeleteButton.onclick = function () {
        deleteSelectedOption('category');
    };
    document.querySelector('label[for="category"]').appendChild(categoryDeleteButton);

    const itemDeleteButton = document.createElement('button');
    itemDeleteButton.textContent = '🗑️';
    itemDeleteButton.onclick = function () {
        deleteSelectedOption('item');
    };
    document.querySelector('label[for="item"]').appendChild(itemDeleteButton);

    // Function to delete the selected category or item
    function deleteSelectedOption(type) {
        const selectedValue = document.getElementById(type).value;
        if (!selectedValue || selectedValue === 'newCategory' || selectedValue === 'newItem') {
            alert('Please select a valid category or item to delete.');
            return;
        }

        if (confirm(`Are you sure you want to delete this ${type}? This action cannot be undone.`)) {
            const actionType = type === 'category' ? 'deleteCategory' : 'deleteItem';
            fetch('warehouse_management.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `action=${actionType}&id=${selectedValue}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`${type.charAt(0).toUpperCase() + type.slice(1)} deleted successfully.`);
                    if (type === 'category') {
                        fetchCategories(); // Reload categories
                    } else {
                        const categoryId = document.getElementById('category').value;
                        fetchItems(categoryId); // Reload items for the current category
                    }
                } else {
                    displayError(data.message || `Error deleting ${type}.`);
                }
            })
            .catch(error => displayError(`Error deleting ${type}.`));
        }
    }
});
