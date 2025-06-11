document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling with loading indicator
    const resumeForm = document.querySelector('form[action*="analyze_resume"]');
    
    if (resumeForm) {
        resumeForm.addEventListener('submit', function(e) {
            const fileInput = this.querySelector('input[type="file"]');
            const submitButton = this.querySelector('button[type="submit"]');
            
            // Check if a file is selected
            if (fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please select a resume file to upload.');
                return;
            }
            
            // Check file type
            const file = fileInput.files[0];
            if (!file.type.match('application/pdf')) {
                e.preventDefault();
                alert('Please upload a PDF file only.');
                return;
            }
            
            // Check file size (max 16MB)
            const maxSize = 16 * 1024 * 1024; // 16MB in bytes
            if (file.size > maxSize) {
                e.preventDefault();
                alert('File size exceeds 16MB. Please upload a smaller file.');
                return;
            }
            
            // Show loading indicator
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing...';
            submitButton.disabled = true;
            
            // Add a progress container after the form
            const progressContainer = document.createElement('div');
            progressContainer.className = 'mt-3';
            progressContainer.innerHTML = `
                <div class="alert alert-info">
                    <div class="d-flex align-items-center">
                        <strong>Processing your resume...</strong>
                        <div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>
                    </div>
                    <div class="progress mt-2" style="height: 5px;">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%"></div>
                    </div>
                </div>
            `;
            
            resumeForm.after(progressContainer);
            
            // Animate progress bar
            const progressBar = progressContainer.querySelector('.progress-bar');
            setTimeout(() => {
                progressBar.style.width = '100%';
            }, 100);
        });
    }
    
    // Initialize tooltips if Bootstrap's JS is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Fade out flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert:not(.alert-info)');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                const closeButton = message.querySelector('.btn-close');
                if (closeButton) {
                    closeButton.click();
                } else {
                    message.classList.add('fade');
                    setTimeout(() => {
                        message.remove();
                    }, 500);
                }
            });
        }, 5000);
    }
});
