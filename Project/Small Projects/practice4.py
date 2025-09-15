from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

#khai báo bảng dữ liêu
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    #mối quan hệ
    author_of_book = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    published_date = Column(Date)

    #Mối quan hệ
    author = relationship("Author", back_populates="author_of_book")

#tạo bảng
Base.metadata.create_all(engine)

#tạo session
Session = sessionmaker(bind=engine)
session = Session()

#Thêm 2 tác giả vào Authors
author1 = Author(name='Huy', country='Viet Nam')
author2 = Author(name='Vu', country='America')
session.query(Author).delete()
session.add_all([author2, author1])
session.commit()
author_table = session.query(Author).all()
for author_data in author_table:
    print(f"ID: {author_data.id}, Name: {author_data.name}, Country: {author_data.country}")

#Thêm 4 cuôn sách, mỗi tác giả ít nhất 2 cuốn
book_data =[
    Book(book_id=1, title='Ngày xưa có một con bò', author_id=author2.id, published_date=date(2022, 12, 1)),
    Book(book_id=2, title='cha giàu cha nghèo', author_id=author2.id, published_date=date(2023, 12, 1)),
    Book(book_id=3, title='khuyến học', author_id=author1.id, published_date=date(2021, 12, 1)),
    Book(book_id=4, title='dạy con làm giàu', author_id=author1.id, published_date=date(2020, 12, 1)),
]
session.query(Book).delete()
session.add_all(book_data)
session.commit()

id_author_query = int(input("Nhập id tác giả: "))
author = session.query(Author).filter_by(id=id_author_query).first()


if author:
    print(f"Những cuốn sách của tác giả {author.name} là ")
    for book in author.author_of_book:
        print(f"-- Sách ID: {book.book_id}, tiêu đề: {book.title}, xuất bản ngày {book.published_date}")
else:
    print("Không tìm thấy tác giả")

#Truy vấn tất cả các tác giả và số lượng sách mà họ đã viết
# book_of_author = session.query(Author).join(Book).group_by(Book.author_id).count(Book.book_id).all()
book_of_author = session.query(Author.name, func.count(Book.book_id)).join(Book).group_by(Author.id).all()
print("Số lượng sách của các tác giả là")
for name, count in book_of_author:
    print(f"-- {name}: {count} sách")
