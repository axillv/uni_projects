document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('submitRescuer'); // Reference the button by its ID

    button.addEventListener('click', function (event) { // Attach the event listener to the button
        event.preventDefault(); // Prevent the default button action (which is to submit the form)

        // Get the values from the input fields
        const username = document.getElementById('usernameR').value;
        const password = document.getElementById('passwordR').value;

        console.log(username);
        console.log(password);

        // Perform basic validation (optional but recommended)
        if (!username || !password) {
            alert('Παρακαλώ εισάγετε το όνομα χρήστη και τον κωδικό πρόσβασης.');
            return;
        }

        // Create an AJAX request to send the data to the server
        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'create_rescuer.php', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        // Define what happens when the server responds
        xhr.onload = function () {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                    alert('Ο λογαριασμός διασώστη δημιουργήθηκε επιτυχώς!');
                    document.getElementById('newDiasosths').reset(); // Clear the form fields
                } else {
                    alert('Σφάλμα: ' + response.message);
                }
            } else {
                alert('Η αίτηση απέτυχε. Κωδικός σφάλματος: ' + xhr.status);
            }
        };

        // Send the form data to the server
        const data = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
        xhr.send(data);
    });
});
