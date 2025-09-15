import psycopg2
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

# Kết nối vào PostgreSQL
conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Danh sách các schema và bảng để người dùng chọn
schemas = ["msx_data", "mst_data"]
tables = {
    "msx_data": [
        "msx_jnt_230321878_data",
        "msx_flash_230321878_data"
    ],
    "mst_data": [
        "mst_jnt_230321878_data",
        "mst_flash_230321878_data"
    ]
}


# Tạo cửa sổ Tkinter để người dùng lựa chọn schema và bảng
def delete_data():
    # Lấy schema, bảng và ngày từ lựa chọn người dùng
    selected_schema = schema_var.get()
    selected_table = table_var.get()
    selected_date = date_var.get()

    if selected_schema and selected_table and selected_date:
        try:
            # Chuyển đổi ngày theo định dạng yyyy-mm-dd
            query = f"DELETE FROM {selected_schema}.{selected_table} WHERE \"Input Date\" = %s;"
            cur.execute(query, (selected_date,))

            # Cam kết thay đổi và đóng kết nối
            conn.commit()
            messagebox.showinfo("Success",
                                f"Data has been deleted from {selected_schema}.{selected_table} on {selected_date}.")
            print(f"Data has been deleted from {selected_schema}.{selected_table} on {selected_date}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Selection Error", "Please select schema, table, and date.")


def update_tables(*args):
    # Cập nhật bảng khi schema được chọn
    selected_schema = schema_var.get()
    table_menu['menu'].delete(0, 'end')

    if selected_schema in tables:
        for table in tables[selected_schema]:
            table_menu['menu'].add_command(label=table, command=tk._setit(table_var, table))


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Delete Data from Table")

# Tạo biến để lưu lựa chọn
schema_var = tk.StringVar(root)
table_var = tk.StringVar(root)
date_var = tk.StringVar(root)

# Tạo OptionMenu cho schema
schema_label = tk.Label(root, text="Choose Schema:")
schema_label.pack(pady=5)

schema_menu = tk.OptionMenu(root, schema_var, *schemas)
schema_menu.pack(pady=5)

# Cập nhật bảng khi schema thay đổi
schema_var.trace("w", update_tables)

# Tạo OptionMenu cho bảng (ban đầu sẽ trống)
table_label = tk.Label(root, text="Choose Table:")
table_label.pack(pady=5)

table_menu = tk.OptionMenu(root, table_var, "")
table_menu.pack(pady=5)

# Tạo Label và Calendar để chọn ngày
date_label = tk.Label(root, text="Choose Date (YYYY-MM-DD):")
date_label.pack(pady=5)

# Calendar để người dùng chọn ngày
calendar = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
calendar.pack(pady=5)


# Lấy ngày từ calendar
def get_date():
    date_var.set(calendar.get_date())


# Nút để lấy ngày từ calendar
get_date_button = tk.Button(root, text="Select Date", command=get_date)
get_date_button.pack(pady=5)

# Tạo nút xóa dữ liệu
delete_button = tk.Button(root, text="Delete Data", command=delete_data)
delete_button.pack(pady=20)

# Chạy giao diện Tkinter
root.mainloop()

# Đóng con trỏ và kết nối
cur.close()
conn.close()
