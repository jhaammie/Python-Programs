

function response(){
        const url = `http://127.0.0.1:5006/getfruit`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    let displaylist = ''
    for (let item in data){
    displaylist += `<li>${data[item]}</li>`
    }
    document.getElementById('tag').innerHTML = displaylist;
    })
    }
window.addEventListener("load", response());
