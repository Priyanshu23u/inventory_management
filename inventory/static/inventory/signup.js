document.getElementById("signupForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("signupMessage");

    message.textContent = "Creating account...";
    message.style.color = "gray";

    const res = await fetch("/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.status === 201) {
        message.textContent = "✅ Signup successful! Redirecting...";
        message.style.color = "green";
        setTimeout(() => window.location.href = "/login/", 1500);
    } else {
        message.textContent = "❌ Signup failed: " + JSON.stringify(data);
        message.style.color = "red";
    }
});
