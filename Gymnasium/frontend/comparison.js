let meritChart = null;
let placesChart = null;
const colors = [
  "rgb(75, 192, 192)",
  "rgb(255, 99, 132)",
  "rgb(54, 162, 235)",
  "rgb(255, 206, 86)",
  "rgb(153, 102, 255)",
];

document.addEventListener("DOMContentLoaded", async () => {
  const selectedSchools = JSON.parse(
    localStorage.getItem("selectedSchools") || "[]"
  );
  if (selectedSchools.length < 2) {
    alert("Välj minst 2 skolor för att jämföra");
    window.close();
    return;
  }

  // Fetch data for all selected schools
  const schoolData = await Promise.all(
    selectedSchools.map((school) =>
      apiGet(`/api/school-details/${encodeURIComponent(school)}`)
    )
  );

  // Create merit score chart
  createMeritChart(schoolData);

  // Create places chart
  createPlacesChart(schoolData);

  // Create detailed comparison table
  createComparisonTable(schoolData);
});

function createMeritChart(schoolData) {
  const ctx = document.getElementById("meritChart").getContext("2d");

  const datasets = [];
  schoolData.forEach((data, index) => {
    const schoolName =
      data.historical_data[0]?.school_name || `Skola ${index + 1}`;

    // Get unique years across all data
    const years = [...new Set(data.historical_data.map((d) => d.year))].sort();

    // Create dataset for preliminary merit
    datasets.push({
      label: `${schoolName} - Preliminär`,
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.year === year);
        return yearData ? yearData.prelim_merit : null;
      }),
      borderColor: colors[index],
      backgroundColor: colors[index] + "40",
      tension: 0.1,
    });

    // Create dataset for final merit
    datasets.push({
      label: `${schoolName} - Slutlig`,
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.year === year);
        return yearData ? yearData.final_merit : null;
      }),
      borderColor: colors[index],
      borderDash: [5, 5],
      backgroundColor: colors[index] + "20",
      tension: 0.1,
    });
  });

  meritChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [
        ...new Set(
          schoolData.flatMap((data) => data.historical_data.map((d) => d.year))
        ),
      ].sort(),
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

function createPlacesChart(schoolData) {
  const ctx = document.getElementById("placesChart").getContext("2d");

  const datasets = [];
  schoolData.forEach((data, index) => {
    const schoolName =
      data.historical_data[0]?.school_name || `Skola ${index + 1}`;

    // Get unique years across all data
    const years = [...new Set(data.historical_data.map((d) => d.year))].sort();

    // Create dataset for available places
    datasets.push({
      label: schoolName,
      data: years.map((year) => {
        const yearData = data.historical_data.find((d) => d.year === year);
        return yearData ? yearData.prelim_available : null;
      }),
      backgroundColor: colors[index],
      borderColor: colors[index],
      borderWidth: 1,
    });
  });

  placesChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [
        ...new Set(
          schoolData.flatMap((data) => data.historical_data.map((d) => d.year))
        ),
      ].sort(),
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Tillgängliga platser över tid",
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

function createComparisonTable(schoolData) {
  const container = document.getElementById("schoolDetails");
  let html =
    '<div class="table-responsive"><table class="table table-bordered">';

  // Table header
  html += "<thead><tr><th>Mätvärde</th>";
  schoolData.forEach((data, index) => {
    const schoolName =
      data.historical_data[0]?.school_name || `Skola ${index + 1}`;
    html += `<th>${schoolName}</th>`;
  });
  html += "</tr></thead><tbody>";

  // Get the latest data for each school
  const latestData = schoolData.map((data) => data.historical_data[0]);

  // Add rows for each metric
  const metrics = [
    { key: "municipality", label: "Kommun" },
    { key: "organization", label: "Organisationsform" },
    { key: "prelim_merit", label: "Preliminärt meritvärde" },
    { key: "final_merit", label: "Slutligt meritvärde" },
    { key: "prelim_places", label: "Preliminära platser" },
    { key: "final_places", label: "Slutliga platser" },
    { key: "prelim_accepted", label: "Preliminärt antagna" },
    { key: "final_accepted", label: "Slutligt antagna" },
    { key: "prelim_reserves", label: "Preliminära reserver" },
    { key: "final_reserves", label: "Slutliga reserver" },
    { key: "prelim_available", label: "Preliminära lediga platser" },
    { key: "final_available", label: "Slutliga lediga platser" },
  ];

  metrics.forEach((metric) => {
    html += `<tr><td>${metric.label}</td>`;
    latestData.forEach((data) => {
      html += `<td>${data[metric.key] || "NA"}</td>`;
    });
    html += "</tr>";
  });

  html += "</tbody></table></div>";
  container.innerHTML = html;
}
