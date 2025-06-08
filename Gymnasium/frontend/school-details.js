// Format value to one decimal place or return 'NA' if null/undefined
function formatValue(value) {
  if (value === null || value === undefined) {
    return "NA";
  }
  return Number(value).toFixed(1);
}

// Store chart instances
const programCharts = {};

// Create a chart for a program
function createProgramCharts(programData, programCode, programName) {
  const container = document.createElement("div");
  container.className = "program-section mb-4";
  container.innerHTML = `
    <h4 class="mb-3">${programName} (${programCode})</h4>
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Meritvärden</h5>
            <canvas id="meritChart_${programCode}" height="300"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Platser</h5>
            <canvas id="placesChart_${programCode}" height="300"></canvas>
          </div>
        </div>
      </div>
    </div>
  `;
  document.getElementById("programSections").appendChild(container);

  // Create merit chart
  const meritCtx = document
    .getElementById(`meritChart_${programCode}`)
    .getContext("2d");
  programCharts[`merit_${programCode}`] = new Chart(meritCtx, {
    type: "line",
    data: {
      labels: programData.map((d) => d.Year),
      datasets: [
        {
          label: "Preliminär merit",
          data: programData.map((d) => d.PreliminaryMerit ?? 0),
          borderColor: "#4e73df",
          backgroundColor: "rgba(78, 115, 223, 0.1)",
          borderWidth: 2,
          tension: 0.1,
        },
        {
          label: "Preliminär median",
          data: programData.map((d) => d.PreliminaryMedian ?? 0),
          borderColor: "#4e73df",
          backgroundColor: "rgba(78, 115, 223, 0.1)",
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.1,
        },
        {
          label: "Slutlig merit",
          data: programData.map((d) => d.FinalMerit ?? 0),
          borderColor: "#1cc88a",
          backgroundColor: "rgba(28, 200, 138, 0.1)",
          borderWidth: 2,
          tension: 0.1,
        },
        {
          label: "Slutlig median",
          data: programData.map((d) => d.FinalMedian ?? 0),
          borderColor: "#1cc88a",
          backgroundColor: "rgba(28, 200, 138, 0.1)",
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Meritvärden över tid",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        y: {
          min: 0,
          max: 340,
          ticks: {
            stepSize: 50,
          },
        },
      },
    },
  });

  // Create places chart
  const placesCtx = document
    .getElementById(`placesChart_${programCode}`)
    .getContext("2d");
  programCharts[`places_${programCode}`] = new Chart(placesCtx, {
    type: "line",
    data: {
      labels: programData.map((d) => d.Year),
      datasets: [
        {
          label: "Antal platser preliminär",
          data: programData.map((d) => d.Antal_platser_prelim ?? 0),
          borderColor: "#4e73df",
          backgroundColor: "rgba(78, 115, 223, 0.1)",
          borderWidth: 2,
          tension: 0.1,
        },
        {
          label: "Antal platser slutlig",
          data: programData.map((d) => d.Antal_platser_final ?? 0),
          borderColor: "#4e73df",
          backgroundColor: "rgba(78, 115, 223, 0.1)",
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.1,
        },
        {
          label: "Antagna preliminär",
          data: programData.map((d) => d.Antagna_prelim ?? 0),
          borderColor: "#1cc88a",
          backgroundColor: "rgba(28, 200, 138, 0.1)",
          borderWidth: 2,
          tension: 0.1,
        },
        {
          label: "Antagna slutlig",
          data: programData.map((d) => d.Antagna_final ?? 0),
          borderColor: "#1cc88a",
          backgroundColor: "rgba(28, 200, 138, 0.1)",
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.1,
        },
        {
          label: "Reserver preliminär",
          data: programData.map((d) => d.Reserver_prelim ?? 0),
          borderColor: "#f6c23e",
          backgroundColor: "rgba(246, 194, 62, 0.1)",
          borderWidth: 2,
          tension: 0.1,
        },
        {
          label: "Reserver slutlig",
          data: programData.map((d) => d.Reserver_final ?? 0),
          borderColor: "#f6c23e",
          backgroundColor: "rgba(246, 194, 62, 0.1)",
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.1,
        },
        {
          label: "Lediga platser preliminär",
          data: programData.map((d) => d.Lediga_platser_prelim ?? 0),
          borderColor: "#e74a3b",
          backgroundColor: "rgba(231, 74, 59, 0.1)",
          borderWidth: 2,
          tension: 0.1,
        },
        {
          label: "Lediga platser slutlig",
          data: programData.map((d) => d.Lediga_platser_final ?? 0),
          borderColor: "#e74a3b",
          backgroundColor: "rgba(231, 74, 59, 0.1)",
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Platser över tid",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        y: {
          min: 0,
          max: 100,
          ticks: {
            stepSize: 20,
          },
        },
      },
    },
  });
}

// Fetch and display school details
async function fetchSchoolDetails() {
  const urlParams = new URLSearchParams(window.location.search);
  const schoolName = urlParams.get("school");

  if (!schoolName) {
    alert("Inget skola angivet");
    return;
  }

  try {
    const data = await apiPost("/api/school-details", {
      school_name: schoolName,
    });
    const school = data.historical_data[0];

    // Update page title
    document.title = `${school.Name} - Skoldetaljer`;

    // Update school information
    document.getElementById("schoolName").textContent = school.Name;
    document.getElementById("municipality").textContent = school.Kommun;

    // Update Google Maps link
    const locationLink = document.getElementById("locationLink");
    alert(data.location);
    if (data.location && data.location.latitude && data.location.longitude) {
      locationLink.href = `https://www.google.com/maps?q=${data.location.latitude},${data.location.longitude}`;
    } else {
      locationLink.style.display = "none";
    }

    // Group historical data by program
    const programData = {};
    data.historical_data.forEach((entry) => {
      const key = `${entry.Studievagskod}_${entry.Studievag}`;
      if (!programData[key]) {
        programData[key] = {
          code: entry.Studievagskod,
          name: entry.Studievag,
          data: [],
        };
      }
      programData[key].data.push(entry);
    });

    // Sort data by year for each program
    Object.values(programData).forEach((program) => {
      program.data.sort((a, b) => a.Year - b.Year);
    });

    // Create charts for each program
    Object.values(programData).forEach((program) => {
      createProgramCharts(program.data, program.code, program.name);
    });
  } catch (error) {
    console.error("Error fetching school details:", error);
    alert("Kunde inte hämta skoldetaljer");
  }
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", fetchSchoolDetails);
