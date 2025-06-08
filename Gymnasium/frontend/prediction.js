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
  console.log("Displaying predictions:", predictions);

  const container = document.getElementById("predictionsContainer");
  const predictionsList = document.getElementById("predictionsList");
  console.log("Container found:", container);
  console.log("PredictionsList found:", predictionsList);

  if (!container || !predictionsList) {
    console.error("Required containers not found!");
    return;
  }

  // Clear existing content
  predictionsList.innerHTML = "";

  if (!predictions || predictions.length === 0) {
    console.log("No predictions to display");
    predictionsList.innerHTML =
      "<p class='text-center'>Inga skolor hittades inom det angivna avståndet</p>";
    container.style.display = "block";
    return;
  }

  console.log("Number of predictions:", predictions.length);

  // Create a row for the cards
  const row = document.createElement("div");
  row.className = "row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4";

  predictions.forEach((pred, index) => {
    console.log(`Processing prediction ${index}:`, pred);

    const col = document.createElement("div");
    col.className = "col";

    const card = document.createElement("div");
    card.className = "card h-100 prediction-card";

    // Calculate probability based on prelim score and final score
    const probability =
      pred.Antagningsgrans_prelim <= pred.Antagningsgrans_final ? 100 : 0;

    // Calculate confidence based on available data
    const confidence = pred.Antal_platser_final > 0 ? 100 : 0;

    // Calculate confidence level class
    let confidenceClass = "confidence-low";
    if (confidence >= 70) {
      confidenceClass = "confidence-high";
    } else if (confidence >= 40) {
      confidenceClass = "confidence-medium";
    }

    // Calculate probability class
    let probabilityClass = "confidence-low";
    if (probability >= 70) {
      probabilityClass = "confidence-high";
    } else if (probability >= 40) {
      probabilityClass = "confidence-medium";
    }

    const cardContent = `
      <div class="card-body">
        <h5 class="card-title">${pred.Name}</h5>
        <h6 class="card-subtitle mb-3 text-muted">${pred.Kommun}</h6>
        <div class="card-text">
          <div class="mb-2">
            <strong>Studievägskod:</strong><br>
            <span class="text-muted">${pred.Studievagskod}</span>
          </div>
          <div class="mb-2">
            <strong>Studieväg:</strong><br>
            <span class="text-muted">${pred.Studievag}</span>
          </div>
          <div class="row mb-2">
            <div class="col-6">
              <strong>Chans att komma in:</strong><br>
              <span class="${probabilityClass}">${probability}%</span>
            </div>
            <div class="col-6">
              <strong>Tillförlitlighet:</strong><br>
              <span class="${confidenceClass}">${confidence}%</span>
            </div>
          </div>
          <div class="mb-2">
            <strong>Avstånd:</strong><br>
            <span>${pred.distance?.toFixed(1) || "N/A"} km</span>
          </div>
        </div>
      </div>
    `;

    console.log(`Card content for ${index}:`, cardContent);

    card.innerHTML = cardContent;
    col.appendChild(card);
    row.appendChild(col);
  });

  predictionsList.appendChild(row);
  container.style.display = "block";
  console.log("Predictions display completed");
}
