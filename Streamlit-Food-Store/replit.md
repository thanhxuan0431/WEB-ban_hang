# Website Bán Đồ Ăn Online

## Overview
Đây là ứng dụng web bán đồ ăn online được xây dựng bằng Streamlit với đầy đủ frontend, backend và database PostgreSQL.

## Tech Stack
- **Frontend**: Streamlit với custom CSS
- **Backend**: Python + Streamlit
- **Database**: PostgreSQL với SQLAlchemy ORM
- **Packages**: streamlit, sqlalchemy, psycopg2-binary, pillow

## Project Structure
```
├── app.py              # Main Streamlit application
├── database.py         # Database connection and session management
├── models.py           # SQLAlchemy ORM models (Food, Order, OrderItem)
├── seed_data.py        # Script to seed initial food data
├── .streamlit/
│   └── config.toml     # Streamlit server configuration
```

## Database Schema
### Foods table
- id, name, description, price, category, image_url, is_available, created_at

### Orders table
- id, customer_name, customer_phone, customer_address, total_amount, status, created_at

### Order_items table
- id, order_id, food_id, food_name, quantity, price

## Features
1. **Menu Page**: Hiển thị danh sách món ăn, lọc theo danh mục, thêm vào giỏ hàng
2. **Cart Page**: Quản lý giỏ hàng, điều chỉnh số lượng, đặt hàng
3. **Admin Page**: 
   - Quản lý món ăn (thêm/xóa/cập nhật trạng thái)
   - Quản lý đơn hàng (xem chi tiết, cập nhật trạng thái)

## Running the Application
```bash
streamlit run app.py --server.port 5000
```

## Order Status Flow
pending → confirmed → preparing → delivering → completed/cancelled
