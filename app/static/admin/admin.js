const params = new URLSearchParams(location.search);
const restaurantId = Number(params.get('restaurant_id') || 1);
let categories = [];

function showTab(id){
  document.querySelectorAll('.tab').forEach(t=>t.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
  if(id==='orders') loadOrders();
  if(id==='products') loadProducts();
  if(id==='clients') loadClients();
}
const fmt = n => Number(n).toLocaleString('ru-RU');

async function loadOrders(){
  const orders = await fetch(`/api/admin/orders/${restaurantId}`).then(r=>r.json());
  document.getElementById('orders').innerHTML = orders.map(o=>`
    <div class="card">
      <div class="row"><h3>Заказ №${o.order_number}</h3><span class="status">${o.status}</span></div>
      <p><b>${o.client_name}</b> · ${o.phone || '-'}</p>
      <p>${o.items.map(i=>`${i.name} × ${i.qty}`).join('<br>')}</p>
      <p><b>${fmt(o.total_sum)} сум</b></p>
      <p class="muted">${o.delivery_type} · ${o.payment_method}<br>${o.address || ''}<br>${o.comment || ''}</p>
      <select onchange="changeStatus(${o.id}, this.value)">
        ${['new','accepted','cooking','ready','delivery','done','cancelled'].map(s=>`<option value="${s}" ${o.status===s?'selected':''}>${s}</option>`).join('')}
      </select>
    </div>`).join('') || '<p>Заказов пока нет</p>';
}
async function changeStatus(orderId, status){
  await fetch(`/api/admin/orders/${orderId}/status`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify({status})});
  await loadOrders();
}
async function loadProducts(){
  categories = await fetch(`/api/admin/categories/${restaurantId}`).then(r=>r.json());
  document.getElementById('pCategory').innerHTML = categories.map(c=>`<option value="${c.id}">${c.name}</option>`).join('');
  const products = await fetch(`/api/admin/products/${restaurantId}`).then(r=>r.json());
  document.getElementById('productsList').innerHTML = products.map(p=>`
    <div class="card">
      <h3>${p.name}</h3>
      <p>${p.description || ''}</p>
      <b>${fmt(p.price)} сум</b>
      <p class="muted">active: ${p.is_active}</p>
    </div>`).join('');
}
async function createProduct(){
  const payload = {
    restaurant_id: restaurantId,
    category_id: Number(document.getElementById('pCategory').value),
    name: document.getElementById('pName').value,
    description: document.getElementById('pDesc').value,
    price: Number(document.getElementById('pPrice').value),
    image_url: '',
    is_active: true
  };
  await fetch('/api/admin/products', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  document.getElementById('pName').value=''; document.getElementById('pDesc').value=''; document.getElementById('pPrice').value='';
  await loadProducts();
}
async function loadClients(){
  const clients = await fetch(`/api/admin/clients/${restaurantId}`).then(r=>r.json());
  document.getElementById('clients').innerHTML = clients.map(c=>`
    <div class="card">
      <h3>${c.name || 'Клиент'}</h3>
      <p>${c.phone || '-'}<br>Telegram ID: ${c.telegram_id}</p>
      <p>Заказов: <b>${c.orders}</b><br>Сумма: <b>${fmt(c.spent)} сум</b></p>
    </div>`).join('') || '<p>Клиентов пока нет</p>';
}
loadOrders();
