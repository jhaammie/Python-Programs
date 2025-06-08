async function getPredictions(event) {
  event.preventDefault();

  const prelimScore = document.getElementById("prelimScore")?.value;
  const radius = document.getElementById("radius")?.value;

  if (!prelimScore || !radius) {
    alert("Vänligen ange både meritvärde och avstånd");
    return;
  }

  try {
    // Get user's location
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject);
    });

    const response = await apiPost(
      `${window.CONFIG.API_BASE_URL}/schools/predictions/regression`,
      {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        radius: parseInt(radius),
        prelim_score: parseFloat(prelimScore),
      }
    );

    displayPredictions(response);
  } catch (error) {
    console.error("Error getting predictions:", error);
    if (error.message.includes("geolocation")) {
      alert(
        "Kunde inte hämta din position. Kontrollera att du har gett tillstånd för plats."
      );
    } else {
      alert(
        "Ett fel uppstod när förutsägelserna skulle hämtas. Försök igen senare."
      );
    }
  }
}

// async function showSchoolDetails(schoolName) {
//   try {
//     const data = await apiGet(`/api/school-details/${schoolName}`);
//     renderSchoolDetails(data);
//   } catch (error) {
//     alert("Kunde inte hämta skoldetaljer: " + error.message);
//   }
// }

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

function displayPredictions(predictions) {
  const container = document.getElementById("predictionsContainer");
  if (!container) return;

  container.innerHTML = "";

  if (!predictions || predictions.length === 0) {
    container.innerHTML =
      "<p class='text-center'>Inga skolor hittades inom det angivna avståndet</p>";
    return;
  }

  const table = document.createElement("table");
  table.className = "table table-striped";

  // Add table header
  const thead = document.createElement("thead");
  thead.innerHTML = `
    <tr>
      <th>Skola</th>
      <th>Kommun</th>
      <th>Studieväg</th>
      <th>Prelim merit</th>
      <th>Predikterad final merit</th>
      <th>Avstånd (km)</th>
    </tr>
  `;
  table.appendChild(thead);

  // Add table body
  const tbody = document.createElement("tbody");
  predictions.forEach((pred) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${pred.Name}</td>
      <td>${pred.Kommun}</td>
      <td>${pred.Studievag}</td>
      <td>${pred.Antagningsgrans_prelim?.toFixed(1) || "N/A"}</td>
      <td>${pred.Antagningsgrans_final?.toFixed(1) || "N/A"}</td>
      <td>${pred.distance?.toFixed(1) || "N/A"}</td>
    `;
    tbody.appendChild(row);
  });
  table.appendChild(tbody);
  container.appendChild(table);
}
