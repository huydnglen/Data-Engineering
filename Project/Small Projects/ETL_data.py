import psycopg2
from psycopg2 import sql

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

# Câu lệnh SQL để lấy dữ liệu và tính toán các chỉ số, sau đó chèn vào bảng mst_flash_230321878_data
sql_insert = """
    INSERT INTO mst_data.mst_flash_230321878_data (
    "Waybill Number", "Sender Name", "Sender Phone", "Receiver Name", "Receiver Phone",
    "Weight (gram)", "Shipping Fee", "Shipping Fee Tax", "COD", "COD Fee", "COD Fee Tax", 
    "Insurance Value", "Insurance Fee", "Return Fee", "Return Fee Tax", "Return Fee Adjustment", "Total Fee", "File Name"
)
SELECT
    msx."Waybill Number",
    msx."Sender Name",
    msx."Sender Phone",
    msx."Receiver Name",
    msx."Receiver Phone",
    msx."Weight (gram)",
    msx."Shipping Fee" / (1 - 0.5) - ((msx."Shipping Fee" / (1 - 0.5)) * (flash_policy.shipping_fee_discount / 100)) AS "Shipping Fee",
    msx."Shipping Fee Tax",
    msx."COD",
    msx."COD" * (flash_policy.cod_fee_discount / 100) AS "COD Fee",
    msx."COD Fee Tax",
    msx."Insurance Value",
    msx."Insurance Fee",
    msx."Return Fee" / (1 - 0.8) AS "Return Fee",
    msx."Return Fee Tax",
    ((msx."Return Fee" / (1 - 0.8)) * (flash_policy.return_fee_discount / 100)) AS "Return Fee Adjustment",
    (
        msx."COD" * (flash_policy.cod_fee_discount / 100) 
        + msx."Insurance Fee" 
        + (msx."Return Fee" / (1 - 0.8) - ((msx."Return Fee" / (1 - 0.8)) * (flash_policy.return_fee_discount / 100))) 
        + (msx."Shipping Fee" / (1 - 0.5) - ((msx."Shipping Fee" / (1 - 0.5)) * (flash_policy.shipping_fee_discount / 100)))
    ) AS "Total Fee",
    msx."File Name"
FROM msx_data.msx_flash_230321878_data msx
JOIN flash_policy ON msx."Sender Name" = flash_policy.warehouse_name;
"""

# Thực thi câu lệnh
cur.execute(sql_insert)

# Cam kết thay đổi
conn.commit()

# Đóng con trỏ và kết nối
cur.close()
conn.close()

print("Data has been successfully inserted into mst_flash_230321878_data.")
