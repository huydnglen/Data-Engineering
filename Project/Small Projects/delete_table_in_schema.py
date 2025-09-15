import psycopg2

# Kết nối với cơ sở dữ liệu PostgreSQL
conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

# Tạo con trỏ để thực thi các lệnh SQL
cur = conn.cursor()

# Lấy danh sách tất cả các bảng trong schema msx_data và mst_data
schemas = ['msx_data', 'mst_data']
for schema in schemas:
    # Lấy tất cả tên bảng trong schema
    cur.execute(f"""
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname = '{schema}'
    """)

    # Lấy kết quả và thực hiện xóa từng bảng
    tables = cur.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"Đang xóa bảng: {schema}.{table_name}")
        cur.execute(f"DROP TABLE IF EXISTS {schema}.{table_name} CASCADE")

# Cam kết (commit) các thay đổi
conn.commit()

# Đóng con trỏ và kết nối
cur.close()
conn.close()

print("Đã xóa tất cả các bảng trong các schema msx_data và mst_data.")
