// Authentication state
let currentUser = null;
let authToken = null;

// Check if user is logged in
function checkAuth() {
  const token = getAuthToken(); // This will now check expiry
  if (token) {
    authToken = token;
    loadUserData();
    updateAuthUI(true);
  } else {
    updateAuthUI(false);
  }
}

// Update UI based on auth state
function updateAuthUI(isLoggedIn) {
  const authButtons = document.getElementById("authButtons");
  const userData = document.getElementById("userData");
  const saveDataBtn = document.getElementById("saveDataBtn");

  if (isLoggedIn) {
    authButtons.innerHTML = `
            <button class="btn btn-outline-danger" onclick="logout()">Logga ut</button>
        `;
    if (userData) userData.style.display = "block";
    if (saveDataBtn) saveDataBtn.style.display = "block";
  } else {
    authButtons.innerHTML = `
            <button class="btn btn-outline-primary me-2" onclick="showLoginModal()">Logga in</button>
            <button class="btn btn-primary" onclick="showRegisterModal()">Registrera</button>
        `;
    if (userData) userData.style.display = "none";
    if (saveDataBtn) saveDataBtn.style.display = "none";
  }
}

// Show login modal
function showLoginModal() {
  const modal = new bootstrap.Modal(document.getElementById("loginModal"));
  modal.show();
}

// Show register modal
function showRegisterModal() {
  const modal = new bootstrap.Modal(document.getElementById("registerModal"));
  modal.show();
}

// Handle login
async function login(event) {
  event.preventDefault();
  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  try {
    const data = await apiPost(`${window.CONFIG.API_BASE_URL}/login`, {
      email,
      password,
    });
    if (data.access_token) {
      // Store token and expiry time
      localStorage.setItem("authToken", data.access_token);
      localStorage.setItem("tokenExpiry", Date.now() + 24 * 60 * 60 * 1000); // 24 hours from now
      authToken = data.access_token;
      currentUser = data.user;
      bootstrap.Modal.getInstance(document.getElementById("loginModal")).hide();
      updateAuthUI(true);
      loadUserData();
    } else {
      throw new Error("Ingen token mottagen från servern");
    }
  } catch (error) {
    alert("Inloggningen misslyckades: " + error.message);
  }
}

// Handle registration
async function register(event) {
  event.preventDefault();
  const email = document.getElementById("registerEmail").value;
  const password = document.getElementById("registerPassword").value;
  const firstName = document.getElementById("registerFirstName").value;
  const lastName = document.getElementById("registerLastName").value;

  try {
    const data = await apiPost("/api/register", {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
    });
    if (data.access_token) {
      // Store token and expiry time
      localStorage.setItem("authToken", data.access_token);
      localStorage.setItem("tokenExpiry", Date.now() + 24 * 60 * 60 * 1000); // 24 hours from now
      authToken = data.access_token;
      currentUser = data.user;
      bootstrap.Modal.getInstance(
        document.getElementById("registerModal")
      ).hide();
      updateAuthUI(true);
    } else {
      throw new Error("Ingen token mottagen från servern");
    }
  } catch (error) {
    alert("Registreringen misslyckades: " + error.message);
  }
}

// Handle logout
function logout() {
  localStorage.removeItem("authToken");
  localStorage.removeItem("tokenExpiry");
  authToken = null;
  currentUser = null;
  updateAuthUI(false);
}

// Load user data
async function loadUserData() {
  if (!authToken) return;

  try {
    const data = await apiGet(`${window.CONFIG.API_BASE_URL}/users/me`);
    currentUser = data;

    if (data.prelim_score) {
      const prelimScoreInput = document.getElementById("prelimScore");
      if (prelimScoreInput) {
        prelimScoreInput.value = data.prelim_score;
      }
    }

    if (data.favorite_schools && data.favorite_schools.length > 0) {
      updateFavoriteSchools(data.favorite_schools);
    }
  } catch (error) {
    console.error("Failed to load user data:", error);
    if (error.message.includes("session")) {
      // Session expired, UI will be updated by handleAuthExpiry
      return;
    }
    alert("Kunde inte ladda användardata: " + error.message);
  }
}

// Get favorite schools from localStorage
function getFavoriteSchools() {
  const favorites = localStorage.getItem("favoriteSchools");
  return favorites ? JSON.parse(favorites) : [];
}

// Save user data to localStorage
async function saveUserData() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Du är inte inloggad. Logga in för att spara dina uppgifter.");
    return;
  }

  const userData = {
    id: localStorage.getItem("userId"),
    email: localStorage.getItem("userEmail"),
    first_name: localStorage.getItem("userFirstName"),
    last_name: localStorage.getItem("userLastName"),
    prelim_score: localStorage.getItem("userPrelimScore"),
    favorite_schools: getFavoriteSchools(),
  };

  try {
    const updatedUser = await apiPut(
      `${window.CONFIG.API_BASE_URL}/users/me`,
      userData
    );
    localStorage.setItem("userEmail", updatedUser.email);
    localStorage.setItem("userFirstName", updatedUser.first_name);
    localStorage.setItem("userLastName", updatedUser.last_name);

    alert("Dina uppgifter har sparats!");
  } catch (error) {
    console.error("Error saving user data:", error);
    alert(
      "Ett fel uppstod när dina uppgifter skulle sparas. Försök igen senare."
    );
  }
}

// Initialize auth on page load
document.addEventListener("DOMContentLoaded", checkAuth);
