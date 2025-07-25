// script.js
function getTokenHeader() {
  const token = localStorage.getItem("access");
  return token ? { "Authorization": "Bearer " + token } : {};
}

// ✅ Helper to get Authorization header
function getAuthHeader() {
  const token = localStorage.getItem("access");
  return token ? { "Authorization": `Bearer ${token}` } : {};
}
 
async function addProduct(name, sku, quantity) {
  const response = await fetch("/products/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeader()  // ✅ Automatically add token here
    },
    body: JSON.stringify({ name, sku, quantity })
  });

  const data = await response.json();
  if (response.ok) {
    alert("Product added successfully!");
  } else {
    alert("Error: " + (data.detail || JSON.stringify(data)));
  }
}
