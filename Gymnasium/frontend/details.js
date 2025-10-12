
window.onload = function () {
  // Get query string parameters
  console.log(window.location)
  console.log(window.location.search)
  const params = new URLSearchParams(window.location.search);
  // Get 'name' value
  const name = params.get("name");
  const id = params.get("id");
  if (id == undefined || id == null) {
    alert("Please produce a valid id");
  } else { GetGymnasiumDetails(id) }

  // If name exists, set it as the title
  if (name) {
    document.title = name;
  }
}

function ShowSchoolDetails(SchoolDetails) {
  document.getElementById("schoolname").innerHTML = SchoolDetails.name
  document.getElementById("kommun").innerHTML = SchoolDetails.kommun
  document.getElementById("ViewInMaps").onclick = () => window.open(`https://www.google.com/maps/search/?api=1&query=${SchoolDetails.latitude},${SchoolDetails.longitude}`)
  labels = SchoolDetails.score.map(item => item.year)
  const years = new Set(Array.from(labels));
  console.log(SchoolDetails.score[0])
  // groupedData = { if (!grouped[d.studievagscod]) grouped[d.studievagscod] = [];
  // grouped[d.studievagscod].push({ x: d.year, y: d.score });}
  grouped = []
  SchoolDetails.score.forEach(item => {
    console.log(item)
    if (!grouped[item.studievägskod]) grouped[item.studievägskod] = [];
    grouped[item.studievägskod].push({ x: item.year, y: item.Antagningsgrans_final });
  }

  )
  console.log(grouped)
  console.log(Object.keys(grouped))
      const datasets = Object.keys(grouped).map((key, idx) => ({
      label: key,
      data: grouped[key].sort((a,b) => a.x - b.x),
      borderColor: `rgb(${idx * 80%255}, ${idx * 90%255}, ${idx * 70%255})`,
      fill: false
    }));

    // Render chart
    new Chart(document.getElementById('schoolChart'), {
      type: 'line',
      data: {
        labels: years,
        datasets: datasets
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Scores by Year and Studievagscod'
          }
        },
        scales: {
          x: {
            title: { display: true, text: 'Year' }
          },
          y: {
            title: { display: true, text: 'Score' },
            beginAtZero: true
          }
        }
      }
    });
}


function GetGymnasiumDetails(id) {
  fetch("http://127.0.0.1:5006/gymnasium/details", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id })
  })

    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(response => ShowSchoolDetails(response))
    .catch(error => console.error("Error:", error));

}
