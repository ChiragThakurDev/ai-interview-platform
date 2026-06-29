from app.db.session import SessionLocal
from app.models.user import User

db=SessionLocal()

try:
    new_user=User(
            name="Chirag",
            email="test123@gmail.com"
            )
    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    print("User inserted successfully!")
    print(f"ID : {new_user.id}")
    print(f"Name : {new_user.name}")
    print(f"Email : {new_user.email}")

except Exception as e:
    db.rollback()
    print("Error :", e)

finally:
    db.close()
