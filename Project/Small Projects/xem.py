import psycopg2

# Kết nối với PostgreSQL
conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

# Tạo con trỏ để thực thi SQL
cur = conn.cursor()

# Truy vấn thông tin cột từ bảng
cur.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE 
      table_name = 'flash_policy';  -- Tên bảng bạn muốn xem cột
""")

# Lấy kết quả và in ra
columns = cur.fetchall()
for column in columns:
    print(column[0])

# Đóng kết nối
cur.close()
conn.close()
