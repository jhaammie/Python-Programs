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
    const data = await apiPost("/api/predict-schools-within-radius", {
      prelimScore,
      radius,
      year,
    });
    renderPredictions(data.predictions);
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
