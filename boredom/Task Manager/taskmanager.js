

function addtask(){
    let aa = document.getElementById('task').value;
    console.log(aa)

    const url = `http://127.0.0.1:5006/addtask`;

    fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: aa })
    })


    }

function reusable(){
 const url = `http://127.0.0.1:5006/fetchingtasks`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    console.log(data)

        let displaylist = ''
    for (let item in data){
    let checked = ''
    const id = data[item]["id"]
    console.log(id)
    if (data[item]["Is_Completed"]){
    checked = "checked"
    }
    displaylist += `<li><input onChange=checkboxclicked(${id}) type="checkbox" ${checked}/>${data[item]["Task"]}</li>`
    }
    document.getElementById('coffee').innerHTML = displaylist;
});

    }

window.addEventListener("load", reusable());

function checkboxclicked(id){
    console.log(id)
    if (event.target.checked) {
        console.log('The checkbox is checked.');
    } else {
        console.log('The checkbox is unchecked.');
    }
   const url = `http://127.0.0.1:5006/tasks/${id}`
 fetch(url, {
        method: "PUT",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "checked":event.target.checked})
    })


}