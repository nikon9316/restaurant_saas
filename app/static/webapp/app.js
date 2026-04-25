const params = new URLSearchParams(location.search);
const restaurantId = Number(params.get('restaurant_id') || 1);
const tg = window.Telegram?.WebApp;
tg?.expand();

let categories = [];
let products = [];
let cart = JSON.parse(localStorage.getItem(`cart_${restaurantId}`) || '[]');

const fmt = n => Number(n).toLocaleString('ru-RU');
const saveCart = () => localStorage.setItem(`cart_${restaurantId}`, JSON.stringify(cart));

async function loadData(){
  const r = await fetch(`/api/restaurant/${restaurantId}`).then(r=>r.json());
  document.getElementById('restaurantName').textContent = r.name;
  document.getElementById('restaurantAddress').textContent = r.address || '';
  document.querySelector('.hero').style.background = r.brand_color || '#111827';

  categories = await fetch(`/api/categories/${restaurantId}`).then(r=>r.json());
  products = await fetch(`/api/products/${restaurantId}`).then(r=>r.json());
  renderCategories();
  renderProducts(products);
  renderCartTotal();
}

function renderCategories(){
  const box = document.getElementById('categories');
  box.innerHTML = `<button class="chip" onclick="renderProducts(products)">Все</button>` +
    categories.map(c => `<button class="chip" onclick="filterCategory(${c.id})">${c.name}</button>`).join('');
}
function filterCategory(id){ renderProducts(products.filter(p => p.category_id === id)); }
function renderProducts(list){
  document.getElementById('products').innerHTML = list.map(p => `
    <div class="card">
      <div class="pic">${p.image_url ? `<img src="${p.image_url}" style="width:100%;height:100%;object-fit:cover;border-radius:14px">` : 'Фото'}</div>
      <h3>${p.name}</h3>
      <p>${p.description || ''}</p>
      <div class="price">${fmt(p.price)} сум</div>
      <button class="add" onclick="addToCart(${p.id})">Добавить</button>
    </div>`).join('');
}
function addToCart(id){
  const p = products.find(x=>x.id===id);
  const item = cart.find(x=>x.product_id===id);
  if(item) item.quantity += 1;
  else cart.push({product_id:id, name:p.name, price:p.price, quantity:1});
  saveCart(); renderCartTotal();
}
function renderCartTotal(){
  const total = cart.reduce((s,i)=>s+i.price*i.quantity,0);
  document.getElementById('cartTotal').textContent = fmt(total);
}
function renderCart(){
  const box = document.getElementById('cartItems');
  box.innerHTML = cart.map((i,idx)=>`
    <div class="cart-row">
      <div><b>${i.name}</b><br>${fmt(i.price)} × ${i.quantity}</div>
      <div>
        <button class="small-btn" onclick="changeQty(${idx},-1)">−</button>
        <button class="small-btn" onclick="changeQty(${idx},1)">+</button>
      </div>
    </div>`).join('') || '<p>Корзина пустая</p>';
  document.getElementById('modalTotal').textContent = fmt(cart.reduce((s,i)=>s+i.price*i.quantity,0));
}
function changeQty(idx,delta){
  cart[idx].quantity += delta;
  if(cart[idx].quantity <= 0) cart.splice(idx,1);
  saveCart(); renderCart(); renderCartTotal();
}

document.getElementById('cartBtn').onclick = () => { renderCart(); document.getElementById('cartModal').classList.remove('hidden'); };
document.getElementById('closeCart').onclick = () => document.getElementById('cartModal').classList.add('hidden');
document.getElementById('sendOrder').onclick = async () => {
  if(cart.length === 0) return alert('Корзина пустая');
  const telegramUser = tg?.initDataUnsafe?.user;
  const payload = {
    restaurant_id: restaurantId,
    telegram_id: telegramUser?.id || 111111,
    name: document.getElementById('name').value || telegramUser?.first_name || 'Гость',
    phone: document.getElementById('phone').value,
    delivery_type: document.getElementById('deliveryType').value,
    address: document.getElementById('address').value,
    payment_method: document.getElementById('paymentMethod').value,
    comment: document.getElementById('comment').value,
    items: cart.map(i=>({product_id:i.product_id, quantity:i.quantity}))
  };
  const res = await fetch('/api/orders', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)}).then(r=>r.json());
  if(res.ok){
    cart=[]; saveCart(); renderCartTotal();
    alert(`Заказ №${res.order_number} принят`);
    tg?.close();
  }
};
loadData();
