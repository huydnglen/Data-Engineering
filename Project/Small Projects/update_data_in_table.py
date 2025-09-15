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

# Đặt tên bảng vào một biến (có thể thay đổi dễ dàng)
table_name = "flash_policy"  # Có thể thay đổi thành "jnt_policy" hoặc bất kỳ bảng nào khác

# Câu lệnh SQL để lấy tất cả dữ liệu từ bảng
cur.execute(f"SELECT * FROM {table_name};")

# Lấy tất cả kết quả từ truy vấn
rows = cur.fetchall()

# In tiêu đề cột
columns = [desc[0] for desc in cur.description]
print("\t".join(columns))

# In từng hàng dữ liệu
for row in rows:
    print("\t".join(map(str, row)))


# 1. Thêm khách hàng mới
def add_customer(clients, warehouse_name, shipping_fee_discount, return_fee_discount, cod_fee_discount, email):
    try:
        cur.execute(f"""
            INSERT INTO {table_name} (clients, warehouse_name, shipping_fee_discount, return_fee_discount, cod_fee_discount, email)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (clients, warehouse_name, shipping_fee_discount, return_fee_discount, cod_fee_discount, email))
        conn.commit()
        print("Customer added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error adding customer: {e}")


# 2. Cập nhật thông tin khách hàng
def update_customer(warehouse_name, clients=None, shipping_fee_discount=None, return_fee_discount=None,
                    cod_fee_discount=None, email=None):
    try:
        # Cập nhật thông tin nếu có
        if clients:
            cur.execute(f"UPDATE {table_name} SET clients = %s WHERE warehouse_name = %s", (clients, warehouse_name))
        if shipping_fee_discount:
            cur.execute(f"UPDATE {table_name} SET shipping_fee_discount = %s WHERE warehouse_name = %s",
                        (shipping_fee_discount, warehouse_name))
        if return_fee_discount:
            cur.execute(f"UPDATE {table_name} SET return_fee_discount = %s WHERE warehouse_name = %s",
                        (return_fee_discount, warehouse_name))
        if cod_fee_discount:
            cur.execute(f"UPDATE {table_name} SET cod_fee_discount = %s WHERE warehouse_name = %s",
                        (cod_fee_discount, warehouse_name))
        if email:
            cur.execute(f"UPDATE {table_name} SET email = %s WHERE warehouse_name = %s", (email, warehouse_name))

        conn.commit()
        print("Customer information updated successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating customer: {e}")


# 3. Xóa khách hàng
def delete_customer(warehouse_name):
    try:
        cur.execute(f"DELETE FROM {table_name} WHERE warehouse_name = %s", (warehouse_name,))
        conn.commit()
        print("Customer deleted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error deleting customer: {e}")


# Ví dụ sử dụng các hàm:

# Thêm khách hàng mới
# add_customer("M95", "MS95 WH", 30.0, 100.00, 1.75, "doisoatbhe@gmail.com")

# # # # Cập nhật thông tin khách hàng (cập nhật email và shipping_fee_discount)
# update_customer("MS89 WH", "M89", 30.00, 70.00, 3.08, "vdggroup2022@gmail.com")

# Xóa khách hàng theo warehouse_name
# delete_customer("MS100 WH")

# Đóng kết nối
cur.close()
conn.close()
