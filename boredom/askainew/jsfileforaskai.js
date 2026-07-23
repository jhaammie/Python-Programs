function askai(){

const userInput = document.getElementById('askai').value;
console.log(userInput)

const value = {
    question:userInput
}

const url = `http://127.0.0.1:5000/question`

fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(value)
})
.then(res => res.json())
.then(data => {
    console.log(data)
    document.getElementById('answer').innerText = data["answerinjson"]; })

}
