   function getLocation(callback) {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            callback(latitude, longitude);
          },
          showError
        );
      } else {
        document.getElementById("location").innerHTML = "Geolocation is not supported by this browser.";
      }
    }

    function getNearestGymnasium(latitude, longitude) {
      fetch("http://127.0.0.1:5006/gymnasium", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude, longitude })
      })
        .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
        .then(renderGymnasiumData)
        .catch(error => console.error("Error:", error));
    }

    function getGymnasiumWithInRadius(latitude, longitude) {
      const radius = document.getElementById("radius").value;
      if (radius <= 0 || radius > 1573) {
        document.getElementById("location").innerHTML = "Enter a valid radius value";
        return;
      }
      const sortBy = document.getElementById("sortBy").value;
      const programOptions = document.getElementById("program").options;
      console.log(programOptions)
      const selectedPrograms = [];
      for (const program of programOptions) {
        if (program.selected) {
          selectedPrograms.push(program.value);
        }
      }
      console.log(selectedPrograms)
      const radios = document.getElementsByName('SortOrder');
      let selectedSortOrder = '';
      for (const radio of radios) {
        if (radio.checked) {
          selectedSortOrder = radio.value;
          break;
        }
      }
      const year = document.getElementById("year").value;
      const minpreMerit = document.getElementById("minPrelimMerit").value;
      const maxpreMerit = document.getElementById("maxPrelimMerit").value;
      const minfinMerit = document.getElementById("minFinalMerit").value;
      const maxfinMerit = document.getElementById("maxFinalMerit").value;

      fetch("http://127.0.0.1:5006/gymnasium-within-radius", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude, longitude, radius, sortBy,
        sortOrder: selectedSortOrder, minpreMerit, maxpreMerit,
        programs: selectedPrograms, year, minfinMerit, maxfinMerit})
      })
        .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
        .then(renderGymnasiumData)
        .catch(error => console.error("Error:", error));
    }

function renderGymnasiumData(data) {
  const listContainer = document.getElementById("GymnasiumListData");
  listContainer.innerHTML = ""; // Clear previous content
  if (!data || data.length === 0) {
    listContainer.innerHTML = "<p class='text-center'>No gymnasium found</p>";
    return;
  }

  const formatValue = (val) => (val != null ? val : 'NA');

  let row = "<div class='row g-4'>";
  for (let i = 0; i < data.length; i++) {
    row += `
    <div class="col-md-6 col-lg-4">
      <div class="card h-100 shadow-sm">
        <div class="card-body">
          <h5 class="card-title">${formatValue(data[i].Name)}</h5>
          <h6 class="card-subtitle mb-2 text-muted">${formatValue(data[i].Kommun)} (${formatValue(data[i].Year)})</h6>
          <p><strong>Studieväg:</strong> ${formatValue(data[i].Studievag)} (${formatValue(data[i].Studievagskod)})</p>
          <p><strong>Organisationsform:</strong> ${formatValue(data[i].Organisitionsform)}</p>

          <div class="table-responsive">
            <table class="table table-bordered table-sm mt-3">
              <thead class="table-light">
                <tr>
                  <th>Uppgift</th>
                  <th>Final</th>
                  <th>Prelim</th>
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
                <tr>
                  <td>Antagna</td>
                  <td>${formatValue(data[i].Antagna_final)}</td>
                  <td>${formatValue(data[i].Antagna_prelim)}</td>
                </tr>
                <tr>
                  <td>Reserver</td>
                  <td>${formatValue(data[i].Reserver_final)}</td>
                  <td>${formatValue(data[i].Reserver_prelim)}</td>
                </tr>
                <tr>
                  <td>Lediga platser</td>
                  <td>${formatValue(data[i].Lediga_platser_final)}</td>
                  <td>${formatValue(data[i].Lediga_platser_prelim)}</td>
                </tr>

              </tbody>
            </table>
            <p><strong>Antagningsgräns skillnad:</strong> ${formatValue(data[i].grans_diff)}</p>
            <p><strong>Median skillnad:</strong> ${formatValue(data[i].median_diff)}</p>
          </div>
        </div>
      </div>
    </div>`;
  }
  row += "</div>";
  listContainer.innerHTML = row;
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
