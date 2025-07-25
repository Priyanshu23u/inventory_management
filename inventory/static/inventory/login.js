// login.js
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem("access", data.access);   // ✅ Store token internally
    localStorage.setItem("refresh", data.refresh);
    window.location.href = "/dashboard/";  // Redirect to dashboard
  } else {
    alert("Login failed: " + (data.detail || "Invalid credentials"));
  }
});
