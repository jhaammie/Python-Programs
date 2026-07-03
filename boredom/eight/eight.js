function addlikes() {

  const url = `http://127.0.0.1:5006/likes`;

  fetch(url, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' }
  })
   .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    getnumberoflikes()
    })

    }





function getnumberoflikes(){
        const url = `http://127.0.0.1:5006/likes`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    console.log(data)
    document.getElementById('numberoflikes').innerText = data;
    })
    }

window.addEventListener("load", getnumberoflikes());
