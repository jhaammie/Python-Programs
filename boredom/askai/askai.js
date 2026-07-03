function askai() {
  const valueofaskai = document.getElementById('askai').value;

  const value = {
    askai: valueofaskai
  };

  const url = `http://127.0.0.1:5006/askai`;

  fetch(url, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(value)
  })
  .then(response => response.text())
    .then(data => {
    console.log(data)
    document.getElementById('aisays').innerText = data;

    })
}

function instructai(text) {
    document.getElementById('askai').value=text;


}