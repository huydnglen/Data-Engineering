import psycopg2
import pandas as pd
from sqlalchemy import create_engine

#kết nối với database sales_db
connection = psycopg2.connect(
    dbname = "sales_db",
    user = "postgres",
    password = "Congchua812@",
    host = "localhost",
    port = "5432"
)

connection.autocommit = True
cursor = connection.cursor()
#xóa bảng
cursor.execute("DROP TABLE IF EXISTS customers CASCADE")
cursor.execute("DROP TABLE IF EXISTS products CASCADE")
cursor.execute("DROP TABLE IF EXISTS orders CASCADE")

#tạo bảng customers
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        region TEXT NOT NULL
    )
""")

#tạo bảng products
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

#tạo bảng orders
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(id),
        product_id INT REFERENCES products(id),
        quantity INT NOT NULL,
        order_date DATE NOT NULL
    )
""")
connection.commit()

#thêm dữ liệu mẫu
cursor.execute("""
INSERT INTO customers (name, email, phone, region) VALUES
    ('Alice', 'alice@gmail.com', '1234567890', 'North'),
    ('Bob', 'bob@gmail.com', '0987654321', 'South'),
    ('Charlie', 'charlie@gmail.com', '1122334455', 'East');
""")

# Thêm dữ liệu vào bảng products
cursor.execute("""
INSERT INTO products (name, price) VALUES
    ('Laptop', 800.0),
    ('Smartphone', 500.0),
    ('Tablet', 300.0);
""")

# Thêm dữ liệu vào bảng orders
cursor.execute("""
INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
    (1, 1, 2, '2024-11-01'),
    (1, 2, 1, '2024-11-10'),
    (2, 3, 5, '2024-11-15'),
    (3, 1, 1, '2024-11-20'),
    (3, 2, 3, '2024-11-25');
""")
connection.commit()

engine = create_engine('postgresql://postgres:Congchua812%40@localhost:5432/sales_db')

query = """
SELECT o.id AS order_id, c.name AS customer_name, c.region, p.name AS product_name,
       o.quantity, p.price, o.quantity * p.price AS total, o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id;
"""

data = pd.read_sql(query, engine)

#tổng doanh thu theo khu vực
total_revenue_by_region = data.groupby('region')['total'].sum()

#top 3 khách hàng mua sắm nhiều nhất
top3_customer = data.groupby('customer_name')['total'].sum().sort_values(ascending=False).head(3)

#sản phẩm bán chạy nhất theo tháng
data['month'] = pd.to_datetime(data['order_date']).dt.to_period('M')
top_product = data.groupby(['month', 'product_name'])['quantity'].sum().reset_index()
top_products_by_month = top_product.sort_values(['month', 'quantity'], ascending=[True, False])

with pd.ExcelWriter('sales_report.xlsx') as writer:
    total_revenue_by_region.to_excel(writer, sheet_name='Revenue by Region')
    top3_customer.to_excel(writer, sheet_name='Top Customers')
    top_products_by_month.to_excel(writer, sheet_name='Top Products by Month')
