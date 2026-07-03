function bundleToObject() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const oof = {
    email: email,
    password: password
  };

  console.log(oof);

  const url = `http://127.0.0.1:5006/LogActivity`;

  fetch(url, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(oof)
  });
}