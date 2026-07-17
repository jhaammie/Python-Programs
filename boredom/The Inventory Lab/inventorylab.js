

function addstuff(){
    let item = document.getElementById('item').value;
    let price = document.getElementById('price').value;
    let quantity = document.getElementById('quantity').value;
    const url = `http://127.0.0.1:5006/addstuff`;

    fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item:item, price:price, quantity:quantity })
    })

    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    console.log(data)
    location.reload()

 });
}


function gettingstuff(){
 const url = `http://127.0.0.1:5006/getstuff`;
    fetch(url, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    console.log(data)

    let displaylist = '  <tr> <th>Item</th> <th>Price</th> <th>Quantity</th> <th>New Quantity</th> <th>Save</th> <th>Delete</th> </tr>'
    for (let i in data){
        let checked = ''
        const id = data[i]["id"]
        const item = data[i]["item"]
        const price = data[i]["price"]
        const quantity = data[i]["quantity"]
        // displaylist += `<li><input onChange=checkboxclicked(${id}) type="checkbox" ${checked}/>${data[item]["Task"]}&nbsp;&nbsp;<button onclick="deleting(${id})">Delete</button></li>`
        displaylist += `<tr> <td>${item}</td> <td>${price}</td> <td>${quantity}</td> <td><input id='${id}' type='number'/></td> <td><button onclick="update(${id})">Update</button></td> <td><button onclick="deleting(${id})">Delete</button></td> </tr>`
        }
    document.getElementById('rowsappendkarnihai').innerHTML = displaylist;
});

    }

window.addEventListener("load", gettingstuff());

function update(id){
    const NewQuantity = document.getElementById(id).value;
    console.log(id)
   const url = `http://127.0.0.1:5006/stuff/${id}`
 fetch(url, {
        method: "PUT",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({'NewQuantity':NewQuantity})
    })
    .then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    console.log(data)
    gettingstuff()
 });


}

function deleting(id){
    console.log(id)
   const url = `http://127.0.0.1:5006/stuff/${id}`
 fetch(url, {
        method: "DELETE",
        headers: { 'Content-Type': 'application/json' }
    })

.then(response => response.ok ? response.json() : response.text().then(Promise.reject))
    .then(data => {
    console.log(data)
    gettingstuff()
});
}
