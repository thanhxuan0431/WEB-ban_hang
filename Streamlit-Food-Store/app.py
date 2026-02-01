import streamlit as st
from database import SessionLocal, init_db
from models import Food, Order, OrderItem
from seed_data import seed_foods

init_db()
seed_foods()

st.set_page_config(
    page_title="Đặt Đồ Ăn Online",
    page_icon="🍜",
    layout="wide"
)

st.markdown("""
<style>
    .food-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .food-card:hover {
        transform: translateY(-5px);
    }
    .price-tag {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    .category-badge {
        background: #4ecdc4;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 12px;
    }
    .cart-item {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stButton>button {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "page" not in st.session_state:
    st.session_state.page = "menu"


def format_price(price):
    return f"{price:,.0f}đ"


def add_to_cart(food_id, food_name, price):
    if food_id in st.session_state.cart:
        st.session_state.cart[food_id]["quantity"] += 1
    else:
        st.session_state.cart[food_id] = {
            "name": food_name,
            "price": price,
            "quantity": 1
        }


def remove_from_cart(food_id):
    if food_id in st.session_state.cart:
        del st.session_state.cart[food_id]


def update_quantity(food_id, quantity):
    if quantity <= 0:
        remove_from_cart(food_id)
    else:
        st.session_state.cart[food_id]["quantity"] = quantity


def get_cart_total():
    return sum(item["price"] * item["quantity"] for item in st.session_state.cart.values())


def get_cart_count():
    return sum(item["quantity"] for item in st.session_state.cart.values())


col1, col2, col3 = st.columns([2, 6, 2])
with col2:
    st.markdown('<p class="header-title">🍜 Nhà Hàng Việt Nam</p>', unsafe_allow_html=True)
    st.markdown("*Đặt đồ ăn ngon, giao hàng nhanh*")

menu_col, cart_col, admin_col = st.columns(3)
with menu_col:
    if st.button("🍽️ Menu", use_container_width=True, type="primary" if st.session_state.page == "menu" else "secondary"):
        st.session_state.page = "menu"
with cart_col:
    cart_count = get_cart_count()
    cart_label = f"🛒 Giỏ hàng ({cart_count})" if cart_count > 0 else "🛒 Giỏ hàng"
    if st.button(cart_label, use_container_width=True, type="primary" if st.session_state.page == "cart" else "secondary"):
        st.session_state.page = "cart"
with admin_col:
    if st.button("⚙️ Quản lý", use_container_width=True, type="primary" if st.session_state.page == "admin" else "secondary"):
        st.session_state.page = "admin"

st.markdown("---")

if st.session_state.page == "menu":
    db = SessionLocal()
    foods = db.query(Food).filter(Food.is_available == True).all()
    db.close()
    
    categories = list(set([f.category for f in foods if f.category]))
    categories.insert(0, "Tất cả")
    
    selected_category = st.selectbox("🔍 Lọc theo danh mục:", categories)
    
    if selected_category != "Tất cả":
        foods = [f for f in foods if f.category == selected_category]
    
    cols = st.columns(3)
    for idx, food in enumerate(foods):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="food-card">
                <span class="category-badge">{food.category or 'Khác'}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if food.image_url:
                st.image(food.image_url, use_container_width=True)
            
            st.markdown(f"### {food.name}")
            st.markdown(f"*{food.description}*")
            st.markdown(f'<span class="price-tag">{format_price(food.price)}</span>', unsafe_allow_html=True)
            
            if st.button(f"➕ Thêm vào giỏ", key=f"add_{food.id}", use_container_width=True):
                add_to_cart(food.id, food.name, food.price)
                st.toast(f"Đã thêm {food.name} vào giỏ hàng!")
                st.rerun()
            
            st.markdown("---")

elif st.session_state.page == "cart":
    st.header("🛒 Giỏ hàng của bạn")
    
    if not st.session_state.cart:
        st.info("Giỏ hàng trống. Hãy thêm món ăn từ menu!")
        if st.button("🍽️ Xem Menu"):
            st.session_state.page = "menu"
            st.rerun()
    else:
        for food_id, item in list(st.session_state.cart.items()):
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
            with col1:
                st.markdown(f"**{item['name']}**")
                st.markdown(f"{format_price(item['price'])} / món")
            with col2:
                new_qty = st.number_input(
                    "Số lượng",
                    min_value=0,
                    value=item["quantity"],
                    key=f"qty_{food_id}",
                    label_visibility="collapsed"
                )
                if new_qty != item["quantity"]:
                    update_quantity(food_id, new_qty)
                    st.rerun()
            with col3:
                subtotal = item["price"] * item["quantity"]
                st.markdown(f"**{format_price(subtotal)}**")
            with col4:
                if st.button("🗑️", key=f"remove_{food_id}"):
                    remove_from_cart(food_id)
                    st.rerun()
            st.markdown("---")
        
        total = get_cart_total()
        st.markdown(f"## 💰 Tổng cộng: {format_price(total)}")
        
        st.markdown("---")
        st.subheader("📝 Thông tin đặt hàng")
        
        with st.form("order_form"):
            customer_name = st.text_input("Họ và tên *")
            customer_phone = st.text_input("Số điện thoại *")
            customer_address = st.text_area("Địa chỉ giao hàng *")
            notes = st.text_area("Ghi chú (không bắt buộc)")
            
            submitted = st.form_submit_button("🛵 Đặt hàng", use_container_width=True, type="primary")
            
            if submitted:
                if not customer_name or not customer_phone or not customer_address:
                    st.error("Vui lòng điền đầy đủ thông tin!")
                else:
                    db = SessionLocal()
                    
                    order = Order(
                        customer_name=customer_name,
                        customer_phone=customer_phone,
                        customer_address=customer_address,
                        total_amount=total,
                        status="pending"
                    )
                    db.add(order)
                    db.commit()
                    db.refresh(order)
                    
                    for food_id, item in st.session_state.cart.items():
                        order_item = OrderItem(
                            order_id=order.id,
                            food_id=food_id,
                            food_name=item["name"],
                            quantity=item["quantity"],
                            price=item["price"]
                        )
                        db.add(order_item)
                    
                    db.commit()
                    db.close()
                    
                    st.session_state.cart = {}
                    st.success(f"🎉 Đặt hàng thành công! Mã đơn hàng: #{order.id}")
                    st.balloons()

elif st.session_state.page == "admin":
    st.header("⚙️ Quản lý nhà hàng")
    
    admin_tab = st.tabs(["📦 Quản lý món ăn", "📋 Quản lý đơn hàng"])
    
    with admin_tab[0]:
        st.subheader("Thêm món ăn mới")
        
        with st.form("add_food_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Tên món ăn *")
                new_price = st.number_input("Giá (VNĐ) *", min_value=0, step=1000)
                new_category = st.selectbox("Danh mục", ["Món chính", "Khai vị", "Món ăn nhanh", "Đồ uống", "Tráng miệng"])
            with col2:
                new_description = st.text_area("Mô tả")
                new_image_url = st.text_input("URL hình ảnh")
                new_available = st.checkbox("Còn hàng", value=True)
            
            add_submitted = st.form_submit_button("➕ Thêm món ăn", use_container_width=True)
            
            if add_submitted:
                if not new_name or new_price <= 0:
                    st.error("Vui lòng nhập tên và giá món ăn!")
                else:
                    db = SessionLocal()
                    new_food = Food(
                        name=new_name,
                        description=new_description,
                        price=new_price,
                        category=new_category,
                        image_url=new_image_url,
                        is_available=new_available
                    )
                    db.add(new_food)
                    db.commit()
                    db.close()
                    st.success(f"Đã thêm món {new_name}!")
                    st.rerun()
        
        st.markdown("---")
        st.subheader("Danh sách món ăn")
        
        db = SessionLocal()
        all_foods = db.query(Food).all()
        db.close()
        
        for food in all_foods:
            with st.expander(f"{food.name} - {format_price(food.price)} {'✅' if food.is_available else '❌'}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**Danh mục:** {food.category}")
                    st.write(f"**Mô tả:** {food.description}")
                with col2:
                    if food.image_url:
                        st.image(food.image_url, width=150)
                with col3:
                    if st.button("🗑️ Xóa", key=f"delete_food_{food.id}"):
                        db = SessionLocal()
                        db.query(Food).filter(Food.id == food.id).delete()
                        db.commit()
                        db.close()
                        st.success("Đã xóa món ăn!")
                        st.rerun()
                    
                    db = SessionLocal()
                    food_item = db.query(Food).filter(Food.id == food.id).first()
                    if food_item:
                        new_status = not food_item.is_available
                        if st.button("🔄 Đổi trạng thái", key=f"toggle_food_{food.id}"):
                            food_item.is_available = new_status
                            db.commit()
                            st.rerun()
                    db.close()
    
    with admin_tab[1]:
        st.subheader("Danh sách đơn hàng")
        
        db = SessionLocal()
        orders = db.query(Order).order_by(Order.created_at.desc()).all()
        
        if not orders:
            st.info("Chưa có đơn hàng nào.")
        else:
            for order in orders:
                status_emoji = {
                    "pending": "⏳",
                    "confirmed": "✅",
                    "preparing": "👨‍🍳",
                    "delivering": "🛵",
                    "completed": "✔️",
                    "cancelled": "❌"
                }.get(order.status, "❓")
                
                with st.expander(f"Đơn #{order.id} - {order.customer_name} - {format_price(order.total_amount)} {status_emoji}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Khách hàng:** {order.customer_name}")
                        st.write(f"**SĐT:** {order.customer_phone}")
                        st.write(f"**Địa chỉ:** {order.customer_address}")
                        st.write(f"**Thời gian:** {order.created_at.strftime('%d/%m/%Y %H:%M')}")
                    
                    with col2:
                        st.write("**Chi tiết đơn hàng:**")
                        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
                        for item in order_items:
                            st.write(f"- {item.food_name} x{item.quantity} = {format_price(item.price * item.quantity)}")
                        st.write(f"**Tổng: {format_price(order.total_amount)}**")
                    
                    new_status = st.selectbox(
                        "Cập nhật trạng thái",
                        ["pending", "confirmed", "preparing", "delivering", "completed", "cancelled"],
                        index=["pending", "confirmed", "preparing", "delivering", "completed", "cancelled"].index(order.status),
                        key=f"status_{order.id}"
                    )
                    
                    if st.button("💾 Lưu", key=f"save_status_{order.id}"):
                        order.status = new_status
                        db.commit()
                        st.success("Đã cập nhật trạng thái!")
                        st.rerun()
        
        db.close()

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🍜 Nhà Hàng Việt Nam - Đặt đồ ăn ngon, giao hàng nhanh</p>
        <p>📞 Hotline: 1900-xxxx | 📧 Email: contact@nhahangvn.com</p>
    </div>
    """,
    unsafe_allow_html=True
)
