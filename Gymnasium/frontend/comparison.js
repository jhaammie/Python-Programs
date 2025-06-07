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
    alert("Please select at least 2 schools to compare");
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
      data.historical_data[0]?.school_name || `School ${index + 1}`;

    // Get unique years across all data
    const years = [...new Set(data.historical_data.map((d) => d.year))].sort();

    // Create dataset for preliminary merit
    datasets.push({
      label: `${schoolName} - Preliminary`,
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
      label: `${schoolName} - Final`,
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
          text: "Merit Scores Over Time",
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
            text: "Merit Score",
          },
        },
        x: {
          title: {
            display: true,
            text: "Year",
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
      data.historical_data[0]?.school_name || `School ${index + 1}`;

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
          text: "Available Places Over Time",
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Number of Places",
          },
        },
        x: {
          title: {
            display: true,
            text: "Year",
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
  html += "<thead><tr><th>Metric</th>";
  schoolData.forEach((data, index) => {
    const schoolName =
      data.historical_data[0]?.school_name || `School ${index + 1}`;
    html += `<th>${schoolName}</th>`;
  });
  html += "</tr></thead><tbody>";

  // Get the latest data for each school
  const latestData = schoolData.map((data) => data.historical_data[0]);

  // Add rows for each metric
  const metrics = [
    { key: "municipality", label: "Municipality" },
    { key: "organization", label: "Organization" },
    { key: "prelim_merit", label: "Preliminary Merit" },
    { key: "final_merit", label: "Final Merit" },
    { key: "prelim_places", label: "Preliminary Places" },
    { key: "final_places", label: "Final Places" },
    { key: "prelim_accepted", label: "Preliminary Accepted" },
    { key: "final_accepted", label: "Final Accepted" },
    { key: "prelim_reserves", label: "Preliminary Reserves" },
    { key: "final_reserves", label: "Final Reserves" },
    { key: "prelim_available", label: "Preliminary Available" },
    { key: "final_available", label: "Final Available" },
  ];

  metrics.forEach((metric) => {
    html += `<tr><td>${metric.label}</td>`;
    latestData.forEach((data) => {
      html += `<td>${data[metric.key] || "N/A"}</td>`;
    });
    html += "</tr>";
  });

  html += "</tbody></table></div>";
  container.innerHTML = html;
}
