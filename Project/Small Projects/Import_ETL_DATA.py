import pandas as pd
import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import filedialog

# Mở giao diện để chọn file Excel
root = tk.Tk()
root.withdraw()  # Ẩn cửa sổ chính của Tkinter

# Mở hộp thoại chọn nhiều file Excel
file_paths = filedialog.askopenfilenames(
    title="Select Excel Files",
    filetypes=[("Excel files", "*.xlsx;*.xls")]
)

if not file_paths:  # Nếu không chọn file nào
    print("No files selected, exiting...")
    exit()

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

# Câu lệnh SQL chèn dữ liệu vào bảng PostgreSQL (bao gồm cột "File Name")
insert_sql = """
    INSERT INTO msx_data.msx_flash_230321878_data (
        "Waybill Number", "Sender Name", "Sender Phone", "Receiver Name", "Receiver Phone",
        "Weight (gram)", "Shipping Fee", "Shipping Fee Tax", "COD", "COD Fee", "COD Fee Tax",
        "Insurance Value", "Insurance Fee", "Return Fee", "Return Fee Tax", "Total Fee", "File Name"
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Lặp qua các tệp đã chọn và xử lý từng tệp
for file_path in file_paths:
    # Đọc danh sách các sheet trong file Excel
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names  # Lấy danh sách tên sheet

    # Lọc ra sheet ngẫu nhiên (không phải "BILLING STATEMENT")
    sheet_to_use = [sheet for sheet in sheet_names if sheet != 'BILLING STATEMENT']

    if not sheet_to_use:  # Nếu không có sheet nào hợp lệ
        print(f"No valid sheet found in file {file_path}, skipping...")
        continue

    # Lấy sheet ngẫu nhiên
    sheet_to_use = sheet_to_use[0]  # Chọn sheet đầu tiên trong danh sách còn lại

    # Đọc dữ liệu từ sheet ngẫu nhiên vào pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_to_use)

    # Lặp qua DataFrame và chèn vào PostgreSQL
    data_to_insert = [
        (
            row['Waybill Number'], row['Sender Name'], row['Sender Phone'], row['Receiver Name'], row['Receiver Phone'],
            row['Weight (gram)'], row['Shipping Fee'], row['Shipping Fee Tax'], row['COD'], row['COD Fee'], row['COD Fee Tax'],
            row['Insurance Value'], row['Insurance Fee'], row['Return Fee'], row['Return Fee Tax'], row['Total Fee'],
            file_path.split('/')[-1]  # Lấy tên file (không bao gồm đường dẫn)
        )
        for index, row in df.iterrows()
    ]

    # Thực thi câu lệnh chèn dữ liệu vào bảng PostgreSQL
    if data_to_insert:
        cur.executemany(insert_sql, data_to_insert)
        print(f"Data from {file_path} has been successfully imported.")
    else:
        print(f"No new data to import from {file_path}, skipping...")

# Sử dụng câu lệnh SQL để loại bỏ dữ liệu trùng lặp trong bảng
remove_duplicates_sql = """
    DELETE FROM msx_data.msx_flash_230321878_data
    WHERE ctid NOT IN (
        SELECT MAX(ctid)
        FROM msx_data.msx_flash_230321878_data
        GROUP BY "Waybill Number", "Sender Name", "Sender Phone", "Receiver Name", "Receiver Phone",
                 "Weight (gram)", "Shipping Fee", "Shipping Fee Tax", "COD", "COD Fee", "COD Fee Tax",
                 "Insurance Value", "Insurance Fee", "Return Fee", "Return Fee Tax", "Total Fee"
    );
"""

# Thực thi câu lệnh loại bỏ dữ liệu trùng lặp
cur.execute(remove_duplicates_sql)
print("Duplicates removed successfully.")

# Cam kết thay đổi và đóng kết nối
conn.commit()

# Chèn vào bảng mst_flash_230321878_data sau khi tính toán các chỉ số
sql_insert_mst = """
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

# Thực thi câu lệnh chèn vào bảng mst_flash_230321878_data
cur.execute(sql_insert_mst)
print("Data has been successfully inserted into mst_flash_230321878_data.")

# Cam kết thay đổi và đóng kết nối
conn.commit()

# Đóng con trỏ và kết nối
cur.close()
conn.close()

print("All data has been successfully processed and inserted.")
