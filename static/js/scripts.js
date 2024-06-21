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
                window.location.href = '/dashboard';  
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred. Please try again.';
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.profile-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            buttons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
});



        // JavaScript to handle form submissions for booking, updating, and canceling accommodations
        document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.book-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const accommodationId = this.querySelector('input[name="accommodation_id"]').value;
            fetch('/book_accommodation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ accommodation_id: accommodationId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                } else {
                    alert('Failed to book accommodation.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while booking accommodation.');
            });
        });
    });

    // Add event listeners for update and cancel buttons
    document.querySelectorAll('.update-button').forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            const accommodationId = form.querySelector('input[name="accommodation_id"]').value;
            fetch(`/get_accommodation/${accommodationId}`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector('#updateModal input[name="accommodation_id"]').value = data.id;
                    document.querySelector('#updateModal input[name="room_number"]').value = data.room_number;
                    document.querySelector('#updateModal input[name="location"]').value = data.location;
                    document.querySelector('#updateModal input[name="type"]').value = data.type;
                    document.querySelector('#updateModal input[name="floor"]').value = data.floor;
                    document.getElementById('updateModal').style.display = 'block';
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while fetching accommodation details.');
                });
        });
    });

    document.querySelectorAll('.cancel-button').forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            const accommodationId = form.querySelector('input[name="accommodation_id"]').value;
            document.querySelector('#cancelModal input[name="accommodation_id"]').value = accommodationId;
            document.getElementById('cancelModal').style.display = 'block';
        });
    });

    // Handle update form submission
    document.getElementById('updateForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const accommodationId = this.querySelector('input[name="accommodation_id"]').value;
        const roomNumber = this.querySelector('input[name="room_number"]').value;
        const location = this.querySelector('input[name="location"]').value;
        const type = this.querySelector('input[name="type"]').value;
        const floor = this.querySelector('input[name="floor"]').value;
        fetch('/update_accommodation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ accommodation_id: accommodationId, room_number: roomNumber, location: location, type: type, floor: floor }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                location.reload();
            } else {
                alert('Failed to update accommodation.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating accommodation.');
        });
    });

    // Handle cancel form submission
    document.getElementById('cancelForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const accommodationId = this.querySelector('input[name="accommodation_id"]').value;
        fetch('/cancel_accommodation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ accommodation_id: accommodationId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                location.reload();
            } else {
                alert('Failed to cancel booking.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while canceling booking.');
        });
    });

    // Handle modal close
    document.querySelectorAll('.modal .close').forEach(span => {
        span.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });
});


