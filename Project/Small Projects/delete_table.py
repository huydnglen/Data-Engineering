import psycopg2

# Kết nối vào PostgreSQL
conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Truy vấn tất cả các bảng trong cơ sở dữ liệu
cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'msx_data';")

# Lấy tất cả các bảng
tables = cur.fetchall()

# In danh sách các bảng để xem
print("Danh sách bảng trong cơ sở dữ liệu:")
for table in tables:
    print(table[0])

# Chọn bảng cần xóa (ví dụ xóa bảng có tên 'your_table_name')
table_to_drop = 'msx_flash_230321878_data'  # Thay thế bằng tên bảng bạn muốn xóa

# Kiểm tra nếu bảng cần xóa có trong danh sách
if (table_to_drop,) in tables:
    # Xóa bảng nếu nó tồn tại trong cơ sở dữ liệu
    cur.execute(f"DROP TABLE IF EXISTS {table_to_drop} CASCADE;")
    conn.commit()
    print(f"Table '{table_to_drop}' has been dropped.")
else:
    print(f"Table '{table_to_drop}' does not exist in the database.")

# Đóng kết nối
cur.close()
conn.close()
# msx_jnt_230321878_data
# msx_jnt_20023519_data
# mst_jnt_20023519_data
# mst_jnt_230321878_data
# mst_flash_230321878_data
# msx_flash_230321878_data