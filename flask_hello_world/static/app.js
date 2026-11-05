// Same-origin request: works on any hostname that routes /api to the Flask backend.
async function fetchApiResponse() {
    const target = document.getElementById('apiResponse');
    try {
        const response = await fetch('/api/hello');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        target.innerText = await response.text();
    } catch (error) {
        target.innerText = `Error: ${error.message}`;
    }
}

window.onload = fetchApiResponse;
