// Format value to one decimal place or return 'NA' if null/undefined
function formatValue(value) {
  if (value === null || value === undefined) {
    return "NA";
  }
  return Number(value).toFixed(1);
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
    if (school.Latitude && school.Longitude) {
      locationLink.href = `https://www.google.com/maps?q=${school.Latitude},${school.Longitude}`;
    } else {
      locationLink.style.display = "none";
    }

    // Populate historical data table
    const historicalData = document.getElementById("historicalData");
    historicalData.innerHTML = data.historical_data
      .map(
        (row) => `
            <tr>
                <td>${row.Year}</td>
                <td>${row.Studievag || "NA"}</td>
                <td>${formatValue(row.Antagningsgrans_prelim)}</td>
                <td>${formatValue(row.Antagningsgrans_final)}</td>
                <td>${formatValue(row.Median_prelim)}</td>
                <td>${formatValue(row.Antal_platser_prelim)}</td>
                <td>${formatValue(row.Antagna_prelim)}</td>
                <td>${formatValue(row.Reserver_prelim)}</td>
                <td>${formatValue(row.Lediga_platser_prelim)}</td>
            </tr>
        `
      )
      .join("");
  } catch (error) {
    console.error("Error fetching school details:", error);
    alert("Kunde inte hämta skoldetaljer");
  }
});
