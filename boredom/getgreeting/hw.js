

function response(){
        const url = `http://127.0.0.1:5006/GetGreeting`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    let ihihi = data

    })
    }
