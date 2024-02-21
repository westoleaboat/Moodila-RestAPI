document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('login-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission
        var accessToken = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
        console.log(accessToken) // correct
        // Serialize form data into JSON object
        var formData = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        };

        // Send form data to the server as JSON
        fetch('/login', { //error
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken // Set bearer token
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                // Handle successful login
                console.log('User logged in successfully.');
                // console.log(response.json)
                // return response.json(); // Parse JSON response
                // window.location.href = '/profile';

            } else {
                throw new Error('Failed to login user');
            }
        })
        .then(data => {
        //     // Store the access token securely (e.g., in local storage)
            localStorage.setItem('accessToken', accessToken);
            console.log(accessToken)

            
        //     // Redirect to the profile page
            window.location.href = '/profile';
        })
        .catch(error => {
            // Handle errors
            console.error('Error logging in user:', error);
            // Optionally, display an error message to the user
        });
    });

});

  // Accessing the profile
    // fetch('/profile', {
    //     method: 'GET',
    //     headers: {
    //         'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
    //     }
    // })
    // .then(response => {
    //     if (response.ok) {
    //         return response.json();
    //     } else {
    //         throw new Error('Failed to fetch user profile');
    //     }
    // })
    // .then(data => {
    //     console.log('User profile:', data);
    // })
    // .catch(error => {
    //     console.error('Error fetching user profile:', error);
    // });



// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('login-form').addEventListener('submit', function (event) {
//         event.preventDefault(); // Prevent default form submission
//         // Retrieve access token from cookie
//         var accessToken = document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
//         // console.log(accessToken)

//         // Serialize form data into JSON object
//         var formData = {
//             username: document.getElementById('username').value,
//             password: document.getElementById('password').value
//         };

//         // Send form data to the server as JSON with bearer token
//         fetch('/login', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': 'Bearer ' + accessToken // Set bearer token
//             },
//             body: JSON.stringify(formData)
//         })
//         .then(response => {
//             if (response.ok) {
//                 // Handle successful login
//                 console.log('User logged in successfully.');
//                 console.log(accessToken)
//                 // Optionally, redirect to another page or show a success message
//                 // window.location.href = '/profile';
//                 // localStorage.setItem('accessToken', accessToken);
            
//                 // Redirect to the profile page
//                 // window.location.href = '/profile';
//                 // return response.json();
//             } else {
//                 throw new Error('Failed to login user');
//             }
//         })
//         .then(data => {
//             // Store the access token securely (e.g., in local storage or a cookie)
//             // localStorage.setItem('accessToken', accessToken);
            
//             // // Redirect to the profile page
//             // window.location.href = '/profile';
//         })
//         .catch(error => {
//             // Handle errors
//             console.error('Error logging in user:', error);
//             // Optionally, display an error message to the user
//         });
//     });
// });
