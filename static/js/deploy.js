document.addEventListener('DOMContentLoaded', function() {
    const deployForm = document.getElementById('deployForm');
    const deployBtn = document.getElementById('deployBtn');
    const deploySpinner = document.getElementById('deploySpinner');
    
    if (deployForm) {
        deployForm.addEventListener('submit', function(e) {
            // Show loading state
            deployBtn.disabled = true;
            deployBtn.innerText = ' Deploying... Please wait';
            deploySpinner.classList.remove('d-none');
            
            // Form submits normally, this just updates UI
        });
    }
    
    // Add validation for the GitHub URL
    const repoUrlInput = document.getElementById('repo_url');
    if (repoUrlInput) {
        repoUrlInput.addEventListener('input', function() {
            const url = repoUrlInput.value.trim();
            
            // Simple validation
            if (url && !url.includes('github.com')) {
                repoUrlInput.setCustomValidity('Please enter a valid GitHub repository URL');
            } else {
                repoUrlInput.setCustomValidity('');
            }
        });
    }
});
