async function getPredictions(event) {
  event.preventDefault();
  const prelimScore = document.getElementById("prelimScore").value;
  const radius = document.getElementById("radius").value;
  const year = document.getElementById("year").value;

  if (!prelimScore || !radius) {
    alert("Vänligen ange både meritvärde och avstånd");
    return;
  }

  try {
    // Get user's location
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject);
    });

    const data = await apiPost("/api/schools/predictions/regression", {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      radius: parseInt(radius),
      prelim_score: parseFloat(prelimScore),
    });

    renderPredictions(data);
  } catch (error) {
    alert("Kunde inte hämta förutsägelser: " + error.message);
  }
}

async function showSchoolDetails(schoolName) {
  try {
    const data = await apiGet(`/api/school-details/${schoolName}`);
    renderSchoolDetails(data);
  } catch (error) {
    alert("Kunde inte hämta skoldetaljer: " + error.message);
  }
}

function getConfidenceLevel(scoreDiff, availablePlaces) {
  // Calculate confidence based on score difference and available places
  if (scoreDiff > 10 && availablePlaces > 5) {
    return { level: "high", text: "Hög - Mycket sannolikt att bli antagen" };
  } else if (scoreDiff > 5 && availablePlaces > 3) {
    return { level: "medium", text: "Medel - God chans att bli antagen" };
  } else if (scoreDiff > 0 && availablePlaces > 0) {
    return { level: "low", text: "Låg - Kan bli antagen" };
  } else {
    return { level: "low", text: "Mycket låg - Osannolikt att bli antagen" };
  }
}

function renderPredictions(predictions) {
  const container = document.getElementById("predictionsContainer");
  container.innerHTML = "";

  if (!predictions || predictions.length === 0) {
    container.innerHTML =
      "<p class='text-center'>Inga skolor hittades inom det angivna avståndet</p>";
    return;
  }

  const table = document.createElement("table");
  table.className = "table table-striped";
  table.innerHTML = `
    <thead>
      <tr>
        <th>Skola</th>
        <th>Kommun</th>
        <th>Studieväg</th>
        <th>Prelim merit</th>
        <th>Predikterad final merit</th>
        <th>Avstånd (km)</th>
      </tr>
    </thead>
    <tbody></tbody>
  `;

  const tbody = table.querySelector("tbody");
  predictions.forEach((pred) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${pred.Name}</td>
      <td>${pred.Kommun}</td>
      <td>${pred.Studievag}</td>
      <td>${pred.Antagningsgrans_prelim}</td>
      <td>${pred.Antagningsgrans_final.toFixed(1)}</td>
      <td>${pred.distance}</td>
    `;
    tbody.appendChild(row);
  });

  container.appendChild(table);
}
