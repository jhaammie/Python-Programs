function feedback() {
  const feedback = document.getElementById('feedback').value;

  const feed = {
    feedback: feedback
  };

  console.log(feed);

  const url = `http://127.0.0.1:5006/feedback`;

  fetch(url, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feed)
  })
  .then(response => response.text())
    .then(data => {
    console.log(data)
    if (parseInt(data) >= 0) {
     document.getElementById('feedback').value = '';
    }
    })
}