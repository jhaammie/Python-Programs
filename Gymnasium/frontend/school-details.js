// Format value to one decimal place or return 'NA' if null/undefined
function formatValue(value) {
  if (value === null || value === undefined) {
    return "NA";
  }
  return Number(value).toFixed(1);
}

let meritChart = null;
let placesChart = null;

function createMeritChart(data) {
  const ctx = document.getElementById("meritChart").getContext("2d");

  // Get unique years and sort them
  const years = [...new Set(data.historical_data.map((d) => d.Year))].sort();

  // Create datasets for each merit type
  const datasets = [
    {
      label: "Preliminär merit",
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.Year === year);
        return yearData ? yearData.Antagningsgrans_prelim : null;
      }),
      borderColor: "rgb(75, 192, 192)",
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      tension: 0.1,
    },
    {
      label: "Slutlig merit",
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.Year === year);
        return yearData ? yearData.Antagningsgrans_final : null;
      }),
      borderColor: "rgb(255, 99, 132)",
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      tension: 0.1,
    },
    {
      label: "Median merit",
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.Year === year);
        return yearData ? yearData.Median_prelim : null;
      }),
      borderColor: "rgb(54, 162, 235)",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      tension: 0.1,
    },
  ];

  if (meritChart) {
    meritChart.destroy();
  }

  meritChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: years,
      datasets: datasets,
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
          beginAtZero: false,
          title: {
            display: true,
            text: "Meritvärde",
          },
        },
        x: {
          title: {
            display: true,
            text: "År",
          },
        },
      },
    },
  });
}

function createPlacesChart(data) {
  const ctx = document.getElementById("placesChart").getContext("2d");

  // Get unique years and sort them
  const years = [...new Set(data.historical_data.map((d) => d.Year))].sort();

  // Create datasets for each places type
  const datasets = [
    {
      label: "Antal platser",
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.Year === year);
        return yearData ? yearData.Antal_platser_prelim : null;
      }),
      borderColor: "rgb(75, 192, 192)",
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      tension: 0.1,
    },
    {
      label: "Antagna",
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.Year === year);
        return yearData ? yearData.Antagna_prelim : null;
      }),
      borderColor: "rgb(255, 99, 132)",
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      tension: 0.1,
    },
    {
      label: "Tillgängliga platser",
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.Year === year);
        return yearData ? yearData.Lediga_platser_prelim : null;
      }),
      borderColor: "rgb(54, 162, 235)",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      tension: 0.1,
    },
  ];

  if (placesChart) {
    placesChart.destroy();
  }

  placesChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: years,
      datasets: datasets,
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
          beginAtZero: true,
          title: {
            display: true,
            text: "Antal platser",
          },
        },
        x: {
          title: {
            display: true,
            text: "År",
          },
        },
      },
    },
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  // Get school name from URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const schoolName = urlParams.get("school");

  if (!schoolName) {
    alert("Ingen skola vald");
    window.location.href = "index.html";
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
    if (school.location.latitide && school.location.longitude) {
      locationLink.href = `https://www.google.com/maps?q=${school.location.latitude},${school.location.longitude}`;
    } else {
      locationLink.style.display = "none";
    }

    // Create charts
    createMeritChart(data);
    createPlacesChart(data);
  } catch (error) {
    console.error("Error fetching school details:", error);
    alert("Kunde inte hämta skoldetaljer");
  }
});
