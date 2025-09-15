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

# Tạo bảng với tên cột giống như trong file Excel
cur.execute("""
    CREATE TABLE IF NOT EXISTS mst_data.mst_jnt_230321878_data (
        "Waybill Number" VARCHAR(255),
        "Sender Name" VARCHAR(255),
        "Sender Phone" VARCHAR(255),
        "Receiver Name" VARCHAR(255),
        "Receiver Phone" VARCHAR(255),
        "Weight (gram)" INTEGER,  -- Trọng lượng (gram) là số nguyên
        "Shipping Fee" DECIMAL(12, 2),  -- Phí vận chuyển (kiểu số thực, 12 chữ số tổng cộng, 2 chữ số thập phân)
        "Shipping Fee Tax" DECIMAL(12, 2),
        "COD" DECIMAL(12, 2),  -- COD (Tiền thu hộ)
        "COD Fee" DECIMAL(12, 2),
        "COD Fee Tax" DECIMAL(12, 2),
        "Insurance Value" DECIMAL(12, 2),
        "Insurance Fee" DECIMAL(12, 2),
        "Return Fee" DECIMAL(12, 2),
        "Return Fee Tax" DECIMAL(12, 2),
        "Return Fee Adjustment" DECIMAL(12, 2),
        "Total Fee" DECIMAL(12, 2)  -- Tổng phí
    )
""")
cur.execute("""
ALTER TABLE mst_data.mst_jnt_230321878_data
ADD COLUMN IF NOT EXISTS "Input Date" DATE,
ADD COLUMN IF NOT EXISTS "File Name" TEXT;
""")
# Đóng con trỏ và kết nối
cur.close()
conn.commit()
conn.close()

print("Table has been successfully created with column names matching the Excel file.")
