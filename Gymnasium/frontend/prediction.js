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

  // Create a row for the cards
  const row = document.createElement("div");
  row.className = "row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4";

  predictions.forEach((pred) => {
    const col = document.createElement("div");
    col.className = "col";

    const card = document.createElement("div");
    card.className = "card h-100";

    // Calculate probability based on prelim score and final score
    const probability =
      pred.Antagningsgrans_prelim >= pred.Antagningsgrans_final ? 100 : 0;

    // Calculate confidence based on available data
    const confidence = pred.Antal_platser_prelim > 0 ? 100 : 0;

    // Calculate confidence level color
    let confidenceColor = "text-danger";
    if (confidence >= 70) {
      confidenceColor = "text-success";
    } else if (confidence >= 40) {
      confidenceColor = "text-warning";
    }

    // Calculate probability color
    let probabilityColor = "text-danger";
    if (probability >= 70) {
      probabilityColor = "text-success";
    } else if (probability >= 40) {
      probabilityColor = "text-warning";
    }

    card.innerHTML = `
      <div class="card-body">
        <h5 class="card-title">${pred.Name}</h5>
        <h6 class="card-subtitle mb-2 text-muted">${pred.Kommun}</h6>
        <p class="card-text">
          <strong>Studieväg:</strong> ${pred.Studievag}<br>
          <strong>Prelim merit:</strong> ${
            pred.Antagningsgrans_prelim?.toFixed(1) || "N/A"
          }<br>
          <strong>Predikterad final merit:</strong> ${
            pred.Antagningsgrans_final?.toFixed(1) || "N/A"
          }<br>
          <strong>Chans att komma in:</strong> <span class="${probabilityColor}">${probability}%</span><br>
          <strong>Tillförlitlighet:</strong> <span class="${confidenceColor}">${confidence}%</span><br>
          <strong>Avstånd:</strong> ${pred.distance?.toFixed(1) || "N/A"} km
        </p>
      </div>
      <div class="card-footer">
        <small class="text-muted">
          Antal platser: ${pred.Antal_platser_prelim || "N/A"} | 
          Antagna: ${pred.Antagna_prelim || "N/A"} | 
          Lediga: ${pred.Lediga_platser_prelim || "N/A"}
        </small>
      </div>
    `;

    col.appendChild(card);
    row.appendChild(col);
  });

  container.appendChild(row);
}
