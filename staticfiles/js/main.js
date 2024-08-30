document.addEventListener('DOMContentLoaded', function() {
     // Functionality for delete confirmation
     const deleteForms = document.querySelectorAll('.delete-form');

     if (deleteForms.length > 0) {
         deleteForms.forEach(form => {
             form.addEventListener('submit', function(event) {
                 if (!confirm('Are you sure you want to delete this quiz?')) {
                     event.preventDefault();
                 }
             });
         });
     }

     setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500); // Remove after fade-out
            }, 5000); // 5 seconds delay before hiding
        });
    }, 1000); // 1 second delay to ensure messages are rendered
});