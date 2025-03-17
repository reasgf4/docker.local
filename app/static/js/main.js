/**
 * Docker Container Manager - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });

    // Add confirmation to dangerous actions
    const dangerousForms = document.querySelectorAll('form[data-confirm]');
    dangerousForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const message = form.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });

    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Add copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const textToCopy = button.getAttribute('data-copy');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(function() {
                    const originalText = button.innerHTML;
                    button.innerHTML = '<i class="bi bi-check"></i> Copied!';
                    setTimeout(function() {
                        button.innerHTML = originalText;
                    }, 2000);
                });
            }
        });
    });

    // Add refresh functionality to refresh buttons
    const refreshButtons = document.querySelectorAll('.btn-refresh');
    refreshButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.location.reload();
        });
    });

    // Add dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
        });

        // Check for saved dark mode preference
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'true') {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }
    }
}); 