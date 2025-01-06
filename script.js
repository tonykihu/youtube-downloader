document.addEventListener('DOMContentLoaded', function() {
    // 1. Get References to HTML Elements
    const downloadButton = document.getElementById('download-button');
    const youtubeUrlInput = document.getElementById('youtube-url');
    const downloadOptionsDiv = document.getElementById('download-options');
    const statusMessage = document.getElementById('status-message');
  
  
    // 2. Add Click Event Listener to the Button
    downloadButton.addEventListener('click', async function() {
      // 3. Get the YouTube URL from the Input Field
      const youtubeUrl = youtubeUrlInput.value;
  
        // 4. Validate URL (Basic Check for Empty Value)
        if (!youtubeUrl.trim()) {
            statusMessage.textContent = "Please enter a YouTube URL.";
            return; // Stop processing
        }
  
      // 5. Show status of processing.
      statusMessage.textContent = 'Processing, please wait...';
  
  
      // 6. Fetch Data from the Python Backend (using asynchronous code)
      try {
        const response = await fetch('/download', { // API endpoint
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ url: youtubeUrl })
        });
  
          // 7. Handle non-ok Response (e.g., 400 or 500)
          if (!response.ok) {
              statusMessage.textContent = 'Error retrieving download options.';
              downloadOptionsDiv.innerHTML = '';
                return; // stop processing
          }
  
  
          // 8. Parse Response JSON
          const data = await response.json();
  
          // 9. Handle Server-side Errors
          if(data.error){
            statusMessage.textContent = data.error;
             downloadOptionsDiv.innerHTML = '';
             return; // stop processing
          }
  
           // 10. Hide any previous error messages
          statusMessage.textContent = "";
  
          // 11. Clear any previous download options.
          downloadOptionsDiv.innerHTML = '';
  
  
          // 12. Dynamically Generate Download Options
          data.formats.forEach(format => {
              const optionDiv = document.createElement('div');
              optionDiv.classList.add('download-option');
              optionDiv.innerHTML = `
                <span>${format.resolution || 'Audio Only'} - ${format.format}</span>
                <a href="${format.download_url}" download>Download</a>
               `;
              downloadOptionsDiv.appendChild(optionDiv); // add new options
          });
      } catch (error) {
        // 13. Handle errors that occur while fetching
          console.error("Error:", error);
          statusMessage.textContent = 'An unexpected error occurred.';
           downloadOptionsDiv.innerHTML = '';
  
      }
    });
  });