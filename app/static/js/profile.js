document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the access token from localStorage
    var accessToken = localStorage.getItem('accessToken');

    console.log(accessToken); // Access token retrieved from localStorage

    // Check if the access token exists
    if (accessToken) {
        // If the access token exists, you can use it to make authenticated requests
        console.log('Access token:', accessToken);

        // Here, you can include your code that requires the access token for JWT authentication

        // For example, you can make a fetch request with the access token in the Authorization header
        fetch('/profile', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + accessToken // Include the access token in the Authorization header
            }
        })
        .then(response => {
            // Handle the response as needed
            if (response.ok) {
                // Handle successful response
                return response.json();
            } else {
                throw new Error('Failed to fetch profile data');
            }
        })
        .then(data => {
            // Handle the profile data
            console.log('Profile data:', data);
        })
        .catch(error => {
            // Handle errors
            console.error('Error fetching profile data:', error);
        });
    } else {
        // If the access token does not exist, the user is not authenticated
        console.log('No access token found. User is not authenticated.');
        // You can redirect the user to the login page or take appropriate action
    }
});
