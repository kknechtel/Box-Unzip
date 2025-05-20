document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('extract-form');
    const extractBtn = document.getElementById('extract-btn');
    const checkboxes = document.querySelectorAll('.file-checkbox');
    const resultsContainer = document.getElementById('extraction-results');

    // Enable/disable extract button based on selections
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateExtractButton);
    });

    function updateExtractButton() {
        const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
        extractBtn.disabled = !anyChecked;
    }

    // Handle form submission with AJAX
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Collect selected file IDs
        const selectedFileIds = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        // Display loading state
        extractBtn.disabled = true;
        extractBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Extracting...';

        // Send AJAX request
        fetch('/extract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file_ids: selectedFileIds }),
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data.results);
            extractBtn.innerHTML = 'Extract Selected Files';
            extractBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error extracting files. Please try again.');
            extractBtn.innerHTML = 'Extract Selected Files';
            extractBtn.disabled = false;
        });
    });

    function displayResults(results) {
        const container = document.getElementById('results-container');
        container.innerHTML = '';

        results.forEach(result => {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'extraction-result mb-3';

            if (result.success) {
                resultDiv.innerHTML = `
                    <h3>${result.name} <span class="badge bg-success">Success</span></h3>
                    <div class="extracted-files">
                        <h4>Extracted ${result.files.length} files:</h4>
                        <ul class="file-list">
                            ${result.files.map(file => `
                                <li>
                                    <a href="/download/${encodeURIComponent(result.extract_path)}/${encodeURIComponent(file.path)}">
                                        ${file.name} (${(file.size / 1024).toFixed(1)} KB)
                                    </a>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `
                    <h3>${result.name || 'Unknown file'} <span class="badge bg-danger">Failed</span></h3>
                    <div class="error-message">Error: ${result.error || 'Unknown error'}</div>
                `;
            }

            container.appendChild(resultDiv);
        });

        resultsContainer.classList.remove('d-none');
    }
});

