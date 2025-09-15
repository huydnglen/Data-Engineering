from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date

#kêt nối với cơ sở dữ liệu
engine = create_engine('sqlite:///library.db')
Base = declarative_base()

#Tạo bảng dữ liệu
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    #Mối quan hệ: one to many
    borrowed_books = relationship("BorrowedBook", back_populates="user")

class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    borrow_date = Column(Date, nullable=False)

    #Quan hệ với bảng user
    user = relationship("User", back_populates="borrowed_books")

#tạo bảng trong cơ sở dưx liệu
Base.metadata.create_all(engine)

#tạo session
Session = sessionmaker(bind=engine)
session = Session()

# 4. Thêm 2 người dùng vào bảng Users
user1 = User(name="Alice", email="alice@example.com")
user2 = User(name="Bob", email="bob@example.com")

session.add_all([user1, user2])
session.commit()

# 5. Thêm sách mượn vào bảng BorrowedBooks
borrowed_books_data = [
    BorrowedBook(book_id=1, user_id=user1.id, borrow_date=date(2023, 5, 1)),
    BorrowedBook(book_id=2, user_id=user1.id, borrow_date=date(2023, 6, 1)),
    BorrowedBook(book_id=3, user_id=user2.id, borrow_date=date(2021, 7, 1)),
    BorrowedBook(book_id=4, user_id=user2.id, borrow_date=date(2022, 8, 1)),
]

session.add_all(borrowed_books_data)
session.commit()

#Tìm tất cả sách mà một người dùng cụ thể(theo id) đã mượn
user_id_to_find = 1
user = session.query(User).filter_by(id=user_id_to_find).first()

if user:
    print(f"Sách mà {user.name} đã mượn")
    for borrowed_book in user.borrowed_books:
        print(f'- Sách ID {borrowed_book.book_id} vào ngày {borrowed_book.borrow_date}')
else:
    print("Không tìm thấy người dùng")

#Tìm tất cả người dùng đã mượn sách từ 2021 trở đi
users_from_2021 = session.query(User).join(BorrowedBook).filter(BorrowedBook.borrow_date >= date(2021, 1, 1)).all()

print("\n người dùng đã mượn sách từ 2021 trở đi:")
for user in users_from_2021:
    print(f"-{user.name} ({user.email})")