from app import app
from database import db
from models.admin import Admin
from werkzeug.security import generate_password_hash
from getpass import getpass


def create_admin():
    username = input("กรอก username: ").strip()
    password = getpass("กรอก password: ").strip()

    if not username or not password:
        print("❌ ห้ามเว้นว่าง")
        return

    existing = Admin.query.filter_by(username=username).first()
    if existing:
        print("❌ username นี้มีอยู่แล้ว")
        return

    new_admin = Admin(username=username, password=generate_password_hash(password))

    db.session.add(new_admin)
    db.session.commit()

    print("✅ สร้าง admin สำเร็จ!")


def delete_admin():
    username = input("กรอก username ที่ต้องการลบ: ").strip()

    admin = Admin.query.filter_by(username=username).first()

    if not admin:
        print("❌ ไม่พบ username นี้ในระบบ")
        return

    confirm = input(f"คุณแน่ใจจะลบ {username}? (y/n): ").lower()
    if confirm != "y":
        print("❌ ยกเลิกการลบ")
        return

    db.session.delete(admin)
    db.session.commit()

    print("✅ ลบ admin สำเร็จ!")


def main():
    with app.app_context():
        while True:
            print("\n=== ADMIN MANAGER ===")
            print("1. สร้าง Admin")
            print("2. ลบ Admin")
            print("3. ออก")

            choice = input("เลือกเมนู: ")

            if choice == "1":
                create_admin()
            elif choice == "2":
                delete_admin()
            elif choice == "3":
                print("👋 ออกจากโปรแกรม")
                break
            else:
                print("❌ เลือกใหม่อีกครั้ง")


if __name__ == "__main__":
    main()
