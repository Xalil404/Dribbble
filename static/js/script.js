//Code to show registration fields by email

document.addEventListener('DOMContentLoaded', function() {
    var emailButton = document.getElementById('email-button');
    var emailFields = document.getElementById('email-fields');
    var signupButton = document.getElementById('signup-button');

    emailButton.addEventListener('click', function() {
        if (emailFields.style.display === 'none') {
            emailFields.style.display = 'block';
            signupButton.style.display = 'block'; // Show the Sign Up button
            emailButton.style.display = 'none'; // Optionally hide the Continue with Email button
        }
    });
});

// JavaScript to hide the loader when the content is loaded
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// JavaScript for pop up to confirm project deletion
document.addEventListener('DOMContentLoaded', function() {
    var deleteModal = document.getElementById('deleteConfirmationModal');
    deleteModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var url = button.getAttribute('data-url'); // Get the URL from data attribute
        var form = deleteModal.querySelector('#deleteForm');
        form.action = url; // Set the form action
        console.log("Delete URL set to:", url); // Debugging
    });
});
