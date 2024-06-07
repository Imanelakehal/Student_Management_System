document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(loginForm);
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                errorMessage.textContent = data.message;
            } else if (data.status === 'success') {
                window.location.href = '/dashboard';  // Change this to your actual dashboard URL
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred. Please try again.';
        });
    });
});
