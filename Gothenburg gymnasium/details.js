window.onload = function () {
  // Get query string parameters
  console.log(window.location)
  console.log(window.location.search)
  const params = new URLSearchParams(window.location.search);
  // Get 'name' value
  const name = params.get("name");

  if (name) {
    document.title = name;
    document.getElementById("schoolname").innerHTML = name;
  }
 }
  function submitFeedback(){
        const feedback = document.getElementById("feedback").value
        const schoolname = document.getElementById("schoolname").value || "Jail"
        const url = `http://127.0.0.1:5006/submit-feedback`;
        fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({schoolname, feedback})
    }) .then(res => {console.log(res); res.json()})
    }