function GetSchools() {
let search = document.getElementById("search").value;

    search = search.trim()
    const url = `http://127.0.0.1:5006/GetSchoolNames?search_query=${encodeURIComponent(search)}`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    let ihihi = data.name
    alert(ihihi)

})

}