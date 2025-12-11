const API = "/api";


async function loadItems() {
  const r = await fetch(`${API}/items`);
  const data = await r.json();
  const ul = document.getElementById("items");
  ul.innerHTML = "";
  data.forEach(i => {
    const li = document.createElement("li");
    li.textContent = i.name;
    ul.appendChild(li);
  });
}


async function addItem() {
  const name = document.getElementById("name").value;
  await fetch(`${API}/items`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name})
  });
  document.getElementById("name").value = "";
  loadItems();
}


loadItems();
