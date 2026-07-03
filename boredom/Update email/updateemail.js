let oldemail = ''
function updateemail() {
  const updateemail = document.getElementById('updateemail').value;

  const update = {
    updateemail: updateemail,
    oldemail: oldemail
  };

  console.log(update);

  const url = `http://127.0.0.1:5006/updateemail`;

  fetch(url, {
      method: "PUT",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(update)
  })
  .then(response => response.text())
    .then(data => {
    console.log(data)
    if (parseInt(data) >= 0) {
     document.getElementById('updateemail').value = '';
    }
    })
}

function getemail(){
        const url = `http://127.0.0.1:5006/getemail`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    laaa = data['email']
    document.getElementById('updateemail').value = laaa;
    oldemail = laaa
    })
    }

window.addEventListener("load", getemail());
