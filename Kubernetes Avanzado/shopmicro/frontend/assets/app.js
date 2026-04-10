function getOrCreateUserId() {
  const storageKey = "shopmicro-user-id";
  const existing = window.localStorage.getItem(storageKey);
  if (existing) {
    return Number(existing);
  }

  const generated = Math.floor(100000 + Math.random() * 900000);
  window.localStorage.setItem(storageKey, String(generated));
  return generated;
}

function renderProductOptions(items) {
  const select = document.getElementById("product-select");
  const currentValue = select.value;
  select.innerHTML = items.map((item) => `
    <option value="${item.id}">
      ${item.name} (${item.price} EUR, stock ${item.stock})
    </option>
  `).join("");

  if (currentValue) {
    select.value = currentValue;
  }
}

async function loadProducts() {
  const response = await fetch("/api/products");
  const payload = await response.json();
  const container = document.getElementById("products");
  const source = document.getElementById("product-source");

  source.textContent = `font: ${payload.source}`;
  renderProductOptions(payload.items);
  container.innerHTML = payload.items.map((item) => `
    <article class="product-card">
      <h3>${item.name}</h3>
      <p>${item.description}</p>
      <strong>${item.price} EUR</strong>
      <p>Stock: ${item.stock}</p>
    </article>
  `).join("");
}

async function createOrder(event) {
  event.preventDefault();
  const form = new FormData(event.target);
  const body = {
    product_id: Number(form.get("product_id")),
    quantity: Number(form.get("quantity")),
    user_id: getOrCreateUserId(),
  };

  const response = await fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const payload = await response.json();
  document.getElementById("order-result").textContent = JSON.stringify(payload, null, 2);
  await loadProducts();
}

document.getElementById("generated-user-id").value = getOrCreateUserId();
document.getElementById("reload-products").addEventListener("click", loadProducts);
document.getElementById("order-form").addEventListener("submit", createOrder);

loadProducts().catch((error) => {
  document.getElementById("products").innerHTML = `<p>Error carregant productes: ${error}</p>`;
});
