from database import SessionLocal, init_db
from models import Food


def seed_foods():
    db = SessionLocal()
    
    existing = db.query(Food).first()
    if existing:
        db.close()
        return
    
    foods = [
        Food(
            name="Phở Bò",
            description="Phở bò truyền thống Hà Nội với nước dùng đậm đà, thịt bò tái chín",
            price=45000,
            category="Món chính",
            image_url="https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=400",
            is_available=True
        ),
        Food(
            name="Bún Chả",
            description="Bún chả Hà Nội với thịt nướng than hoa, bún tươi và nước mắm chua ngọt",
            price=50000,
            category="Món chính",
            image_url="https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400",
            is_available=True
        ),
        Food(
            name="Bánh Mì",
            description="Bánh mì thịt nguội đầy đủ với pate, chả lụa, rau thơm",
            price=25000,
            category="Món ăn nhanh",
            image_url="https://images.unsplash.com/photo-1600688640154-9619e002df30?w=400",
            is_available=True
        ),
        Food(
            name="Cơm Tấm",
            description="Cơm tấm Sài Gòn với sườn nướng, bì, chả, trứng ốp la",
            price=55000,
            category="Món chính",
            image_url="https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400",
            is_available=True
        ),
        Food(
            name="Gỏi Cuốn",
            description="Gỏi cuốn tôm thịt tươi ngon với nước chấm đậu phộng",
            price=35000,
            category="Khai vị",
            image_url="https://images.unsplash.com/photo-1553621042-f6e147245754?w=400",
            is_available=True
        ),
        Food(
            name="Chả Giò",
            description="Chả giò giòn rụm nhân thịt và rau củ",
            price=40000,
            category="Khai vị",
            image_url="https://images.unsplash.com/photo-1544025162-d76694265947?w=400",
            is_available=True
        ),
        Food(
            name="Bò Lúc Lắc",
            description="Bò lúc lắc xào với ớt chuông, hành tây, ăn kèm cơm trắng",
            price=75000,
            category="Món chính",
            image_url="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400",
            is_available=True
        ),
        Food(
            name="Trà Đào",
            description="Trà đào cam sả mát lạnh",
            price=25000,
            category="Đồ uống",
            image_url="https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400",
            is_available=True
        ),
        Food(
            name="Cà Phê Sữa Đá",
            description="Cà phê sữa đá đậm đà kiểu Việt Nam",
            price=20000,
            category="Đồ uống",
            image_url="https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400",
            is_available=True
        ),
        Food(
            name="Chè Ba Màu",
            description="Chè ba màu với đậu xanh, đậu đỏ và thạch",
            price=20000,
            category="Tráng miệng",
            image_url="https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400",
            is_available=True
        ),
    ]
    
    for food in foods:
        db.add(food)
    
    db.commit()
    db.close()


if __name__ == "__main__":
    init_db()
    seed_foods()
    print("Seeded database successfully!")
