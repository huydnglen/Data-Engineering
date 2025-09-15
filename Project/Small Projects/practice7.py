import psycopg2

#kết nối với cở sở dữ liệu
connection = psycopg2.connect(
    dbname = "library",
    user = "postgres",
    password = "Congchua812@",
    host = "localhost",
    port = "5432"
)

#Tạo một cursor để thực thi SQL
cursor = connection.cursor()

#tạo bảng 'readers'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS readers(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

#tạo bảng books
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
""")

#tạo bảng borrowed_books
cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrowed_books (
        reader_id INT REFERENCES readers(id),
        book_id INT REFERENCES books(id),
        borrow_date DATE NOT NULL,
        return_date DATE,
        PRIMARY KEY (reader_id, book_id)
    )
""")

#thêm dữ liệu vào các bảng
cursor.execute("""
    INSERT INTO readers (name, email)
    VALUES
        ('An', 'an@gmail.com'),
        ('Binh', 'binh@gmail.com'),
        ('Cuong', 'cuong@gmail.com'),
        ('Dung', 'dung@gmail.com');
""")

cursor.execute("""
    INSERT INTO books (title, author)
    VALUES 
        ('Learn Python', 'Mark Lutz'),
        ('Python Advanced', 'David Beazley'),
        ('Cooking 101', 'Gordon Ramsay'),
        ('Data Science Basics', 'Joel Grus'),
        ('AI for Beginners', 'Andrew Ng');
""")

cursor.execute("""
    INSERT INTO borrowed_books (reader_id, book_id, borrow_date, return_date)
    VALUES
        (1, 1, '2024-11-20', '2024-11-25'),
        (1, 2, '2024-11-22', NULL),
        (2, 3, '2024-11-23', NULL);
""")

cursor.execute("""
    select r.name, b.title
    FROM readers r
    JOIN borrowed_books bb
    ON r.id = bb.reader_id
    JOIN books b
    ON b.id = bb.book_id
""")
results = cursor.fetchall()
for i in results:
    print(f"{i[0]} : {i[1]}")

cursor.close()
connection.close()