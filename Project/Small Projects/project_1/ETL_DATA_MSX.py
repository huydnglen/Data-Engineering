import pandas as pd
import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import filedialog

# Tạo cửa sổ chọn loại bảng
def select_table_type(selected_type):
    global table_type
    table_type = selected_type
    root.destroy()  # Đóng cửa sổ sau khi chọn

# Hiển thị giao diện chọn bảng
root = tk.Tk()
root.title("Select Table Type")

tk.Label(root, text="Choose the type of data to process:", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Flash", command=lambda: select_table_type('flash'), width=20).pack(pady=5)
tk.Button(root, text="JNT", command=lambda: select_table_type('jnt'), width=20).pack(pady=5)

root.mainloop()

# Kiểm tra xem người dùng đã chọn hay chưa
if 'table_type' not in globals():
    print("No selection made. Exiting...")
    exit()

# Mở giao diện để chọn file Excel
root = tk.Tk()
root.withdraw()  # Ẩn cửa sổ chính của Tkinter
file_paths = filedialog.askopenfilenames(
    title="Select Excel Files",
    filetypes=[("Excel files", "*.xlsx;*.xls")]
)

if not file_paths:
    print("No files selected, exiting...")
    exit()

# Đặt tên bảng dựa trên lựa chọn
if table_type == 'flash':
    source_table = "msx_flash_230321878_data"
    policy_table = "flash_policy"
    target_table = "mst_flash_230321878_data"
elif table_type == 'jnt':
    source_table = "msx_jnt_230321878_data"
    policy_table = "jnt_policy"
    target_table = "mst_jnt_230321878_data"

# Kết nối PostgreSQL
conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Câu lệnh SQL chèn dữ liệu vào bảng nguồn
insert_sql = sql.SQL("""
    INSERT INTO msx_data.{source_table} (
        "Waybill Number", "Sender Name", "Sender Phone", "Receiver Name", "Receiver Phone",
        "Weight (gram)", "Shipping Fee", "Shipping Fee Tax", "COD", "COD Fee", "COD Fee Tax",
        "Insurance Value", "Insurance Fee", "Return Fee", "Return Fee Tax", "Total Fee", "File Name"
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""").format(source_table=sql.Identifier(source_table))

# Xử lý từng file Excel
for file_path in file_paths:
    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names
    sheet_to_use = [sheet for sheet in sheet_names if sheet != 'BILLING STATEMENT']

    if not sheet_to_use:
        print(f"No valid sheet found in file {file_path}, skipping...")
        continue

    sheet_to_use = sheet_to_use[0]
    df = pd.read_excel(file_path, sheet_name=sheet_to_use)

    data_to_insert = [
        (
            row['Waybill Number'], row['Sender Name'], row['Sender Phone'], row['Receiver Name'], row['Receiver Phone'],
            row['Weight (gram)'], row['Shipping Fee'], row['Shipping Fee Tax'], row['COD'], row['COD Fee'], row['COD Fee Tax'],
            row['Insurance Value'], row['Insurance Fee'], row['Return Fee'], row['Return Fee Tax'], row['Total Fee'],
            file_path.split('/')[-1]
        )
        for _, row in df.iterrows()
    ]

    if data_to_insert:
        cur.executemany(insert_sql, data_to_insert)
        print(f"Data from {file_path} has been successfully imported into {source_table}.")
    else:
        print(f"No new data to import from {file_path}, skipping...")

# Loại bỏ dữ liệu trùng lặp trong bảng nguồn
remove_duplicates_sql = sql.SQL("""
    DELETE FROM msx_data.{source_table}
    WHERE ctid NOT IN (
        SELECT MAX(ctid)
        FROM msx_data.{source_table}
        GROUP BY "Waybill Number", "Sender Name", "Sender Phone", "Receiver Name", "Receiver Phone",
                 "Weight (gram)", "Shipping Fee", "Shipping Fee Tax", "COD", "COD Fee", "COD Fee Tax",
                 "Insurance Value", "Insurance Fee", "Return Fee", "Return Fee Tax", "Total Fee"
    );
""").format(source_table=sql.Identifier(source_table))
cur.execute(remove_duplicates_sql)
print(f"Duplicates removed successfully from {source_table}.")

# Định nghĩa các hệ số chiết khấu
if table_type == 'flash':
    shipping_discount = 0.5
    return_discount = 0.8
elif table_type == 'jnt':
    shipping_discount = 0.4
    return_discount = 0  # Nếu cần thay đổi hệ số khác cho JNT, thay đổi tại đây

# Câu lệnh chèn dữ liệu vào bảng đích với các hệ số động
insert_target_sql = sql.SQL("""
    INSERT INTO mst_data.{target_table} (
        "Waybill Number", "Sender Name", "Sender Phone", "Receiver Name", "Receiver Phone",
        "Weight (gram)", "Shipping Fee", "Shipping Fee Tax", "COD", "COD Fee", "COD Fee Tax",
        "Insurance Value", "Insurance Fee", "Return Fee", "Return Fee Tax", "Return Fee Adjustment", "Total Fee", "Input Date", "File Name"
    )
    SELECT
        msx."Waybill Number",
        msx."Sender Name",
        msx."Sender Phone",
        msx."Receiver Name",
        msx."Receiver Phone",
        msx."Weight (gram)",
        msx."Shipping Fee" / (1 - {shipping_discount}) - ((msx."Shipping Fee" / (1 - {shipping_discount})) * (policy.shipping_fee_discount / 100)) AS "Shipping Fee",
        msx."Shipping Fee Tax",
        msx."COD",
        msx."COD" * (policy.cod_fee_discount / 100) AS "COD Fee",
        msx."COD Fee Tax",
        msx."Insurance Value",
        msx."Insurance Fee",
        msx."Return Fee" / (1 - {return_discount}) AS "Return Fee",
        msx."Return Fee Tax",
        ((msx."Return Fee" / (1 - {return_discount})) * (policy.return_fee_discount / 100)) AS "Return Fee Adjustment",
        (
            msx."COD" * (policy.cod_fee_discount / 100) 
            + msx."Insurance Fee" 
            + (msx."Return Fee" / (1 - {return_discount}) - ((msx."Return Fee" / (1 - {return_discount})) * (policy.return_fee_discount / 100))) 
            + (msx."Shipping Fee" / (1 - {shipping_discount}) - ((msx."Shipping Fee" / (1 - {shipping_discount})) * (policy.shipping_fee_discount / 100)))
        ) AS "Total Fee",
        msx."Input Date",
        msx."File Name"
    FROM msx_data.{source_table} msx
    JOIN {policy_table} policy ON msx."Sender Name" = policy.warehouse_name;
""").format(
    target_table=sql.Identifier(target_table),
    source_table=sql.Identifier(source_table),
    policy_table=sql.Identifier(policy_table),
    shipping_discount=sql.Literal(shipping_discount),
    return_discount=sql.Literal(return_discount)
)

cur.execute(insert_target_sql)
print(f"Data has been successfully inserted into {target_table}.")

# Cam kết thay đổi và đóng kết nối
conn.commit()
cur.close()
conn.close()

print("All data has been successfully processed and inserted.")
