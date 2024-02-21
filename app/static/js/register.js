console.log('register!');
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('register-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission
  
        // Serialize form data into JSON object
        var formData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            team: document.getElementById('team').value
        };
  
        // Send form data to the server as JSON
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                // Handle successful registration
                console.log('User registered successfully.');
                // Redirect to the login page
                window.location.href = '/login';
            } else {
                throw new Error('Failed to register user');
            }
        })
        .catch(error => {
            // Handle errors
            console.error('Error registering user:', error);
            // Optionally, display an error message to the user
        });
    });
});