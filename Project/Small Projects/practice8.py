import pandas as pd
import psycopg2
from sqlalchemy import create_engine

#kết nối đến cơ sở dữ liệu
connection = psycopg2.connect(
    dbname = "sales_db",
    user = "postgres",
    password = "Congchua812@",
    host ="localhost",
    port = "5432"
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id SERIAL PRIMARY KEY,
        customer_name TEXT NOT NULL,
        email TEXT NOT NULL,
        region TEXT NOT NULL,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INT NOT NULL,
        order_date DATE NOT NULL
    )
""")
connection.commit()

engine = create_engine('postgresql://postgres:Congchua812%40@localhost:5432/sales_db')

#đọc dữ liệu csv
data = pd.read_csv('F:\\pythonProject2\\sales.csv')

#chèn vào sql
data.to_sql('sales', con=engine, if_exists='append', index=False)

query1 = """
    SELECT region, SUM(price*quantity) AS total_revenue
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC
"""
total_revenue_by_region = pd.read_sql(query1, con=engine)
print("Tổng doanh thu theo khu vực:")
print(total_revenue_by_region)