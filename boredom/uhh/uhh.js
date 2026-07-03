

function response(){
        const url = `http://127.0.0.1:5006/LogActivity`;
    fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    })
    }
