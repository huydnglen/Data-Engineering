from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, func, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

#tạo bảng trung gian
borrowed_books_table = Table(
    'borrowed_books',
    Base.metadata,
    Column('reader_id', Integer, ForeignKey('readers.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('borrow_date', Date, nullable=False),
    Column('return_date', Date, nullable=False)
)

#Tạo các class
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    books = relationship('Book', back_populates='author')
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='books')
    readers = relationship('Reader', secondary=borrowed_books_table, back_populates='books')
class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    books = relationship('Book', secondary=borrowed_books_table, back_populates='readers')

#Tạo bảng
Base.metadata.create_all(engine)

#Thêm dữ liệu

#tạo session
Session = sessionmaker(bind=engine)
session = Session()

#xóa dữ liệu cũ
session.query(Author).delete()
session.query(Book).delete()
session.query(Reader).delete()

#thêm 3 tác giả
#thêm 6 sách
#thêm 4 độc giả
