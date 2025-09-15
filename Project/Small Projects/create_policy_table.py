import psycopg2

# Kết nối đến PostgreSQL
conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

# Tạo con trỏ để thực thi SQL
cur = conn.cursor()

# Tạo bảng flash_policy
create_table_sql = """
CREATE TABLE IF NOT EXISTS jnt_policy (
    clients VARCHAR(50) PRIMARY KEY,
    warehouse_name VARCHAR(255),
    shipping_fee_discount DECIMAL(5, 2),
    return_fee_discount DECIMAL(5, 2),
    cod_fee_discount DECIMAL(5, 2),
    email VARCHAR(255)
);
"""
cur.execute(create_table_sql)
# Chèn dữ liệu vào bảng flash_policy
insert_data_sql = insert_data_sql = """
INSERT INTO jnt_policy (clients, warehouse_name, shipping_fee_discount, return_fee_discount, cod_fee_discount, email)
VALUES
    ('M08', 'MS08 WH', 10.00, 100.00, 3.08, 'Lienmica1011@gmail.com'),
    ('M16', 'MS16 WH', 30.00, 100.00, 2.25, 'kt3tops2023@gmail.com'),
    ('M28', 'MS28 ẢO', 28.00, 100.00, 2.52, 'luuthanhbinh129@gmail.com'),
    ('M29', 'MS29 WH', 0.00, 100.00, 3.08, 'dinhvanduc1605@gmail.com'),
    ('M32', 'MS32 WH', 10.00, 100.00, 3.08, 'nguythitho2000@gmail.com'),
    ('M34', 'MS34 WH', 40.00, 100.00, 2.25, 'tungmoyes1204@gmail.com'),
    ('M44', 'MS44 WH', 40.00, 100.00, 2.00, 'adam@mspeedyfulfillment.com'),
    ('M54', 'MS54 WH', 0.00, 100.00, 3.08, 'iloveinuyashaandkagome@gmail.com'),
    ('M56', 'MS56 WH', 0.00, 100.00, 3.08, 'DTglobal1997@gmail.com'),
    ('M57', 'MS57 WH', 0.00, 100.00, 3.08, 'sunday20h01@gmail.com'),
    ('M61', 'MS61 WH', 0.00, 100.00, 3.08, 'nguyenmisen2312@gmail.com'),
    ('M63', 'MS63 WH', 0.00, 100.00, 3.08, 'tantienthanhson@gmail.com'),
    ('M68', 'MS68 WH', 40.00, 100.00, 2.25, 'Hacanh5@gmail.com'),
    ('M72', 'MS72 WH', 30.00, 100.00, 2.25, 'ketoanfivegrand@gmail.com'),
    ('M73', 'MS73 WH', 30.00, 100.00, 3.08, 'trinhnghiem9.11@gmail.com'),
    ('M76', 'MS76 WH', 20.00, 100.00, 3.08, 'luongtrung.668899@gmail.com'),
    ('M78', 'MS78 WH', 0.00, 100.00, 3.08, 'nhungtran101191@gmail.com'),
    ('M79', 'MS79 WH', 0.00, 100.00, 3.08, 'ntquan3198@gmail.com'),
    ('M82', 'MS82 WH', 0.00, 100.00, 1.50, 'nguyenmisen2312@gmail.com'),
    ('M84', 'MS84 WH', 0.00, 100.00, 3.08, 'toantranquoc.hvtc@gmail.com'),
    ('M88', 'MS88 WH', 0.00, 100.00, 2.25, 'ketoantops2024@gmail.com'),
    ('M86', 'MS86 WH', 0.00, 100.00, 3.08, 'bbluegroup24@gmail.com'),
    ('M89', 'MS89 WH', 30.00, 100.00, 3.08, 'vdggroup2022@gmail.com'),
    ('M90', 'MS90+++', 28.00, 100.00, 2.25, 'luuthanhbinh129@gmail.com'),
    ('M91', 'MS91 WH', 0.00, 100.00, 3.08, 'hathinhungt96@gmail.com'),
    ('M92', 'MS92 WH', 0.00, 100.00, 1.50, 'kt3tops2023@gmail.com'),
    ('M96', 'MS96 WH', 40.00, 100.00, 2.25, 'tungmoyes1204@gmail.com'),
    ('M94', 'MS94 WH', 0.00, 100.00, 3.08, 'hoangduc.ducvinh@gmail.com');
"""


cur.execute(insert_data_sql)

# Cam kết thay đổi
conn.commit()

# Đóng con trỏ và kết nối
cur.close()
conn.close()

print("Dữ liệu đã được chèn thành công vào bảng 'flash_policy'.")
