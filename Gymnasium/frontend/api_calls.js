// api_calls.js

function getAuthToken() {
  const token = localStorage.getItem("authToken");
  if (!token) return null;

  try {
    // Check if token is expired
    const payload = JSON.parse(atob(token.split(".")[1]));
    if (payload.exp * 1000 < Date.now()) {
      handleAuthExpiry();
      return null;
    }
    return token;
  } catch (error) {
    console.error("Error parsing token:", error);
    handleAuthExpiry();
    return null;
  }
}

async function apiGet(url) {
  const token = getAuthToken();
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(url, { headers });

  if (response.status === 401) {
    handleAuthExpiry();
    throw new Error("Din session har gått ut. Vänligen logga in igen.");
  }

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      errorText || "Ett fel uppstod vid kommunikation med servern."
    );
  }

  return response.json();
}

async function apiPost(url, data) {
  const token = getAuthToken();
  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });

  if (response.status === 401) {
    handleAuthExpiry();
    throw new Error("Din session har gått ut. Vänligen logga in igen.");
  }

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      errorText || "Ett fel uppstod vid kommunikation med servern."
    );
  }

  return response.json();
}

function handleAuthExpiry() {
  localStorage.removeItem("authToken");
  if (typeof updateAuthUI === "function") {
    updateAuthUI(false);
  }
  // Show expiry message only if we're not already on the login page
  if (!window.location.pathname.includes("login")) {
    alert("Din session har gått ut. Vänligen logga in igen.");
  }
}

async function apiPut(url, data) {
  const token = localStorage.getItem("token");
  if (!token) {
    throw new Error("No authentication token found");
  }

  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      errorText || "Ett fel uppstod vid kommunikation med servern."
    );
  }

  return response.json();
}
