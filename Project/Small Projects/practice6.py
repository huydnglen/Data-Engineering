from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

# Bảng trung gian BorrowedBooks
borrowed_books_table = Table(
    'borrowed_books',
    Base.metadata,
    Column('reader_id', Integer, ForeignKey('readers.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('borrow_date', Date, nullable=False),
    Column('return_date', Date, nullable=True)
)

# Bảng Authors
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String)

    books = relationship('Book', back_populates='author')

# Bảng Books
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    published_date = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='books')
    readers = relationship('Reader', secondary=borrowed_books_table, back_populates='books')

# Bảng Readers
class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    books = relationship('Book', secondary=borrowed_books_table, back_populates='readers')

# Tạo bảng
Base.metadata.create_all(engine)

from datetime import date

Session = sessionmaker(bind=engine)
session = Session()

# Xóa dữ liệu cũ (nếu có)
session.query(Author).delete()
session.query(Book).delete()
session.query(Reader).delete()

# Thêm tác giả
authors = [
    Author(name='Huy', country='Vietnam'),
    Author(name='Lan', country='USA'),
    Author(name='Minh', country='France')
]

# Thêm sách
books = [
    Book(title='Learn Python', published_date=date(2021, 5, 1), author=authors[0]),
    Book(title='Python Advanced', published_date=date(2022, 6, 10), author=authors[0]),
    Book(title='Cooking 101', published_date=date(2020, 8, 15), author=authors[1]),
    Book(title='Data Science Basics', published_date=date(2019, 12, 1), author=authors[1]),
    Book(title='History of France', published_date=date(2021, 1, 20), author=authors[2]),
    Book(title='Learn SQL', published_date=date(2023, 4, 5), author=authors[2]),
]

# Thêm độc giả
readers = [
    Reader(name='Vu', email='vu@gmail.com'),
    Reader(name='Hien', email='hien@gmail.com'),
    Reader(name='Trang', email='trang@gmail.com'),
    Reader(name='Quang', email='quang@gmail.com')
]

# Gán dữ liệu mượn sách
readers[0].books.append(books[0])  # Vu mượn Learn Python
readers[0].books.append(books[1])  # Vu mượn Python Advanced
readers[1].books.append(books[2])  # Hien mượn Cooking 101
readers[1].books.append(books[3])  # Hien mượn Data Science Basics
readers[2].books.append(books[0])  # Trang mượn Learn Python

session.add_all(authors + books + readers)
session.commit()

books_and_authors = session.query(Book.title, Author.name).join(Author).all()
print("Danh sách sách và tác giả:")
for title, author_name in books_and_authors:
    print(f"- {title} (by {author_name})")

borrowed_books_unreturned = (
    session.query(Reader.name, Book.title)
    .join(borrowed_books_table)
    .join(Book)
    .filter(borrowed_books_table.c.return_date == None)
    .all()
)

print("Danh sách độc giả chưa trả sách:")
for reader_name, book_title in borrowed_books_unreturned:
    print(f"- {reader_name} chưa trả sách '{book_title}'")

unborrowed_books = (
    session.query(Book.title)
    .outerjoin(borrowed_books_table)
    .filter(borrowed_books_table.c.reader_id == None)
    .all()
)

print("Danh sách sách chưa được mượn:")
for book_title, in unborrowed_books:
    print(f"- {book_title}")

most_borrowed_author = (
    session.query(Author.name, func.count(Book.id).label('borrow_count'))
    .join(Book)
    .join(borrowed_books_table)
    .group_by(Author.id)
    .order_by(func.count(Book.id).desc())
    .first()
)

print(f"Tác giả có nhiều sách được mượn nhất là {most_borrowed_author.name}, với {most_borrowed_author.borrow_count} lần mượn.")

month = 5  # Ví dụ: Tháng 5
year = 2021  # Ví dụ: Năm 2021

most_active_reader = (
    session.query(Reader.name, func.count(Book.id).label('book_count'))
    .join(borrowed_books_table)
    .join(Book)
    .filter(func.strftime('%m', borrowed_books_table.c.borrow_date) == str(month).zfill(2))
    .filter(func.strftime('%Y', borrowed_books_table.c.borrow_date) == str(year))
    .group_by(Reader.id)
    .order_by(func.count(Book.id).desc())
    .first()
)

if most_active_reader:
    print(f"Độc giả mượn nhiều sách nhất trong tháng {month}/{year} là {most_active_reader.name}, với {most_active_reader.book_count} sách.")
else:
    print(f"Không có độc giả nào mượn sách trong tháng {month}/{year}.")

start_date = date(2021, 1, 1)
end_date = date(2022, 12, 31)

borrowed_books_in_range = (
    session.query(Book.title, borrowed_books_table.c.borrow_date)
    .join(borrowed_books_table)
    .filter(borrowed_books_table.c.borrow_date.between(start_date, end_date))
    .all()
)

print(f"Sách được mượn từ {start_date} đến {end_date}:")
for book_title, borrow_date in borrowed_books_in_range:
    print(f"- {book_title} (mượn ngày {borrow_date})")
