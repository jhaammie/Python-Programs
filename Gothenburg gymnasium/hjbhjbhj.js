
function GetSchools() {
let search = document.getElementById("search").value;

    search = search.trim()
    const url = `http://127.0.0.1:5006/GetSchoolNames?search_query=${encodeURIComponent(search)}`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    let ihihi = data.name
    let string = ''
      for (let i = 0; i < ihihi.length; i++) {

       string += `<div onclick="OpenPage('${ihihi[i]}')" class="myDiv">`+ihihi[i]+'</div>'
      }
      document.getElementById("ListOfSchools").innerHTML = string

})

}



  function getLocation(OnLocationReceived) {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
         // this is a stupidly formatted callback function which Nisha
          // named anonymous function with the logic that it has no name
          (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            OnLocationReceived(latitude, longitude);
          },
           // this is a stupidly formatted callback function which Nisha
          // named showError
          showError
        );
      } else {
        document.getElementById("location").innerHTML = "Geolocation is not supported by this browser.";
      }
    }


function OpenPage(SchoolName) {
    window.open(`./details.html?name=${SchoolName}`)
        console.log(SchoolName)
}




 function previouspage(){
        if (currentpage>0){
            currentpage = currentpage-1
            getLocation(getGymnasiumWithinRadius)
        }
    }
    function nextpage(){
         currentpage = currentpage+1
         getLocation(getGymnasiumWithinRadius)
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

let currentpage = 0;
let pagesize = 15;
  function getGymnasiumWithinRadius(latitude, longitude) {
        const radius = document.getElementById("radius").value;
        const year = document.getElementById("year").value;
        const sortBy = document.getElementById("sortBy").value;
        const radios = document.getElementsByName('SortOrder');
        const programOptions = document.getElementById('program').options;
        const minmerit = document.getElementById('minPrelimMerit').value;
        const maxmerit = document.getElementById('maxPrelimMerit').value;

         let selectedSortOrder = '';
          for (const radio of radios) {
            if (radio.checked) {
              selectedSortOrder = radio.value;
              break;
            }
          }
          console.log(programOptions)
      const selectedPrograms = [];
      // For every program in program options
      for (const program of programOptions) {
        if (program.selected) {
          selectedPrograms.push(program.value);
        }
      }
      console.log(selectedPrograms)


        fetch("http://127.0.0.1:5006/gymnasium-within-radius", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude, longitude, radius, sortBy,
        sortOrder: selectedSortOrder,
        programs: selectedPrograms, year, minfinMerit:minmerit, maxfinMerit:maxmerit, pageno:currentpage, pagesize})
      })
        .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
        .then(renderGymnasiumData)
        .catch(error => console.error("Error:", error));

    }

    function renderGymnasiumData(data) {
    let string = ''
    console.log(data)
      for (let i = 0; i < data.length; i++) {

       string += "<div  class='myDiv'>"+data[i].Skola+"<br/>"
       +"Studieväg: "+data[i].Studieväg+"<br/>"
       +"AntagningspoängPrelim: "+data[i].AntagningspoängPrelim+"<br/>"
        +"AntagningspoängFinal: "+data[i].AntagningspoängSlut+"<br/>"
        +"MedelvärdePrelim: "+data[i].MedelsvärdePrelim+"<br/>"
       +"MedelvärdeSlut: "+data[i].MedelvärdeSlut+"<br/>"
       +"Antagningspoängreservng: "+data[i].Antagningspoängreservng+"<br/>"
       +"medelvärdeReserv: "+data[i].medelvärdeReserv+"<br/>"
       +"år: "+data[i].år+'</div>'
       document.getElementById("schools").innerHTML = string
      }

    }

