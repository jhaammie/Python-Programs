let currentPage = 0;
const pageSize = 50;
let selectedSchools = new Set();
const MAX_SELECTED_SCHOOLS = 5;

function getLocation(callback) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
      // Store coordinates for pagination
      window.lastLatitude = latitude;
      window.lastLongitude = longitude;
      window.lastPageNumber = currentPage;
      callback(latitude, longitude);
    }, showError);
  } else {
    document.getElementById("location").innerHTML =
      "Geolocation is not supported by this browser.";
  }
}

async function getNearestGymnasium(latitude, longitude) {
  try {
    const data = await apiPost(`${window.CONFIG.API_BASE_URL}/gymnasium`, {
      latitude,
      longitude,
    });
    renderGymnasiumData(data);
  } catch (error) {
    console.error("Error:", error);
    alert("Kunde inte hämta gymnasium: " + error.message);
  }
}

async function getGymnasiumWithInRadius() {
  const radius = document.getElementById("radius").value;
  const sortBy = document.getElementById("sortBy").value;
  const sortOrder = document.querySelector(
    'input[name="SortOrder"]:checked'
  ).value;
  const minpreMerit = document.getElementById("minPrelimMerit").value;
  const maxpreMerit = document.getElementById("maxPrelimMerit").value;
  const minfinMerit = document.getElementById("minFinalMerit").value;
  const maxfinMerit = document.getElementById("maxFinalMerit").value;
  const programs = Array.from(
    document.getElementById("program").selectedOptions
  ).map((option) => option.value);
  const year = document.getElementById("year").value;

  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject);
    });

    const data = await apiPost("/api/gymnasium-within-radius", {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      radius: radius,
      sortBy: sortBy,
      sortOrder: sortOrder,
      minpreMerit: minpreMerit,
      maxpreMerit: maxpreMerit,
      minfinMerit: minfinMerit,
      maxfinMerit: maxfinMerit,
      programs: programs,
      year: year,
      page: currentPage,
      pageSize: pageSize,
    });

    renderGymnasiumData(data.data);
    updatePagination(data.total, data.page, data.pageSize);
  } catch (error) {
    console.error("Fel vid hämtning av gymnasium:", error);
    alert("Kunde inte hämta gymnasium: " + error.message);
  }
}

function handleGymnasiumResponse(response) {
  if (!response || !response.data) {
    renderGymnasiumData([]);
    renderPagination(0, 0);
    return;
  }

  renderGymnasiumData(response.data);
  renderPagination(response.page, response.totalPages);
}

function renderGymnasiumData(data) {
  const listContainer = document.getElementById("GymnasiumListData");
  listContainer.innerHTML = ""; // Clear previous content
  if (!data || data.length === 0) {
    listContainer.innerHTML =
      "<p class='text-center'>Inga gymnasieskolor hittades</p>";
    return;
  }

  const formatValue = (val) => (val != null ? val : "NA");

  let row = "<div class='row g-4'>";
  for (let i = 0; i < data.length; i++) {
    row += `
    <div class="col-md-6 col-lg-4">
      <div class="card h-100 shadow-sm" onclick="showSchoolDetails('${
        data[i].Name
      }')">
        <div class="card-body">
          <h5 class="card-title">${formatValue(data[i].Name)}</h5>
          <h6 class="card-subtitle mb-2 text-muted">${formatValue(
            data[i].Kommun
          )} (${formatValue(data[i].Year)})</h6>
          <p><strong>Studieväg:</strong> ${formatValue(
            data[i].Studievag
          )} (${formatValue(data[i].Studievagskod)})</p>
          <p><strong>Organisationsform:</strong> ${formatValue(
            data[i].Organisitionsform
          )}</p>

          <div class="table-responsive">
            <table class="table table-bordered table-sm mt-3">
              <thead class="table-light">
                <tr>
                  <th>Uppgift</th>
                  <th>Slutlig</th>
                  <th>Preliminär</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Antagningsgräns</td>
                  <td>${formatValue(data[i].Antagningsgrans_final)}</td>
                  <td>${formatValue(data[i].Antagningsgrans_prelim)}</td>
                </tr>
                <tr>
                  <td>Median</td>
                  <td>${formatValue(data[i].Median_final)}</td>
                  <td>${formatValue(data[i].Median_prelim)}</td>
                </tr>
                <tr>
                  <td>Platser</td>
                  <td>${formatValue(data[i].Antal_platser_final)}</td>
                  <td>${formatValue(data[i].Antal_platser_prelim)}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>`;
  }
  row += "</div>";
  listContainer.innerHTML = row;
}

function renderPagination(currentPage, totalPages) {
  const paginationContainer = document.getElementById("pagination");
  if (!paginationContainer) return;

  let paginationHTML = `
    <nav aria-label="Page navigation">
      <ul class="pagination justify-content-center">
        <li class="page-item ${currentPage === 0 ? "disabled" : ""}">
          <a class="page-link" href="#" onclick="changePage(${
            currentPage - 1
          })" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
  `;

  // Show up to 5 page numbers
  let startPage = Math.max(0, currentPage - 2);
  let endPage = Math.min(totalPages - 1, startPage + 4);
  startPage = Math.max(0, endPage - 4);

  for (let i = startPage; i <= endPage; i++) {
    paginationHTML += `
      <li class="page-item ${i === currentPage ? "active" : ""}">
        <a class="page-link" href="#" onclick="changePage(${i})">${i + 1}</a>
      </li>
    `;
  }

  paginationHTML += `
        <li class="page-item ${
          currentPage === totalPages - 1 ? "disabled" : ""
        }">
          <a class="page-link" href="#" onclick="changePage(${
            currentPage + 1
          })" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  `;

  paginationContainer.innerHTML = paginationHTML;
}

function changePage(newPage) {
  currentPage = newPage;
  window.lastPageNumber = newPage;
  // Reuse the last used coordinates
  if (window.lastLatitude && window.lastLongitude) {
    getGymnasiumWithInRadius();
  }
}

function showError(error) {
  let message = "";
  switch (error.code) {
    case error.PERMISSION_DENIED:
      message = "User denied the request for Geolocation.";
      break;
    case error.POSITION_UNAVAILABLE:
      message = "Location information is unavailable.";
      break;
    case error.TIMEOUT:
      message = "The request to get user location timed out.";
      break;
    case error.UNKNOWN_ERROR:
      message = "An unknown error occurred.";
      break;
  }
  document.getElementById("location").innerHTML = message;
}

let historicalChart = null;

async function showSchoolDetails(schoolName) {
  try {
    const response = await apiPost("/api/schools", {
      school_name: schoolName,
    });

    const modal = document.getElementById("schoolDetailsModal");
    const modalBody = modal.querySelector(".modal-body");

    // Create content for the modal
    let content = `
      <div class="mb-4">
        <h5>Skolinformation</h5>
        <p><strong>Skola:</strong> ${response.historical_data[0].Name}</p>
        <p><strong>Kommun:</strong> ${response.historical_data[0].Kommun}</p>
        ${
          response.location.latitude
            ? `
          <p><strong>Plats:</strong> ${response.location.latitude.toFixed(
            6
          )}, ${response.location.longitude.toFixed(6)}</p>
        `
            : ""
        }
      </div>
      <div class="table-responsive">
        <h5>Historisk data</h5>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>År</th>
              <th>Studieväg</th>
              <th>Preliminär merit</th>
              <th>Slutlig merit</th>
              <th>Median preliminär</th>
              <th>Median slutlig</th>
              <th>Antal platser</th>
              <th>Antagna</th>
              <th>Reserver</th>
              <th>Lediga platser</th>
            </tr>
          </thead>
          <tbody>
    `;

    response.historical_data.forEach((data) => {
      content += `
        <tr>
          <td>${data.Year}</td>
          <td>${data.Studievag}</td>
          <td>${
            data.Antagningsgrans_prelim?.toFixed(1) || "Ej tillgänglig"
          }</td>
          <td>${data.Antagningsgrans_final?.toFixed(1) || "Ej tillgänglig"}</td>
          <td>${data.Median_prelim?.toFixed(1) || "Ej tillgänglig"}</td>
          <td>${data.Median_final?.toFixed(1) || "Ej tillgänglig"}</td>
          <td>${data.Antal_platser_prelim || "Ej tillgänglig"}</td>
          <td>${data.Antagna_prelim || "Ej tillgänglig"}</td>
          <td>${data.Reserver_prelim || "Ej tillgänglig"}</td>
          <td>${data.Lediga_platser_prelim || "Ej tillgänglig"}</td>
        </tr>
      `;
    });

    content += `
          </tbody>
        </table>
      </div>
    `;

    modalBody.innerHTML = content;
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
  } catch (error) {
    console.error("Fel vid hämtning av skoldetaljer:", error);
    alert("Kunde inte hämta skoldetaljer: " + error.message);
  }
}

function updatePagination(total, currentPage, pageSize) {
  const totalPages = Math.ceil(total / pageSize);
  const paginationContainer = document.getElementById("pagination");
  paginationContainer.innerHTML = "";

  if (totalPages <= 1) return;

  // Create pagination controls
  const ul = document.createElement("ul");
  ul.className = "pagination justify-content-center";

  // Previous button
  const prevLi = document.createElement("li");
  prevLi.className = `page-item ${currentPage === 0 ? "disabled" : ""}`;
  prevLi.innerHTML = `
        <a class="page-link" href="#" onclick="changePage(${
          currentPage - 1
        })" ${currentPage === 0 ? 'tabindex="-1" aria-disabled="true"' : ""}>
            Föregående
        </a>
    `;
  ul.appendChild(prevLi);

  // Page numbers
  const startPage = Math.max(0, currentPage - 2);
  const endPage = Math.min(totalPages - 1, currentPage + 2);

  for (let i = startPage; i <= endPage; i++) {
    const li = document.createElement("li");
    li.className = `page-item ${i === currentPage ? "active" : ""}`;
    li.innerHTML = `
            <a class="page-link" href="#" onclick="changePage(${i})">
                ${i + 1}
            </a>
        `;
    ul.appendChild(li);
  }

  // Next button
  const nextLi = document.createElement("li");
  nextLi.className = `page-item ${
    currentPage === totalPages - 1 ? "disabled" : ""
  }`;
  nextLi.innerHTML = `
        <a class="page-link" href="#" onclick="changePage(${
          currentPage + 1
        })" ${
    currentPage === totalPages - 1 ? 'tabindex="-1" aria-disabled="true"' : ""
  }>
            Nästa
        </a>
    `;
  ul.appendChild(nextLi);

  paginationContainer.appendChild(ul);
}
