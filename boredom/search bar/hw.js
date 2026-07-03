

function search(){
    let aa = document.getElementById('searchbar').value;
    console.log(aa)
    const url = `http://127.0.0.1:5006/searchbar?search_query=${aa}`;

    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(data => {
    console.log(data)
    let displaylist = ''
    for (let item in data){
    displaylist += `<li>${data[item].name}</li>`
    }
    document.getElementById('coffee').innerHTML = displaylist;

    })
    }
