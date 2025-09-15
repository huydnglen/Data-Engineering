import pandas as pd
from sqlalchemy import create_engine

# Kết nối với PostgreSQL sử dụng SQLAlchemy
engine = create_engine('postgresql+psycopg2://mspeedy:mspeedy@localhost:5432/mspeedy')

# Mở kết nối thủ công (KHÔNG sử dụng with)
conn = engine.raw_connection()

# Truy vấn dữ liệu từ bảng
query = 'SELECT * FROM "mst_data"."mst_flash_230321878_data"'

# Đọc dữ liệu vào pandas DataFrame
df = pd.read_sql(query, conn)

# Đóng kết nối sau khi lấy dữ liệu
conn.close()

# Xuất dữ liệu ra file Excel
output_file = "exported_data.xlsx"
df.to_excel(output_file, index=False)

print(f"Dữ liệu đã được xuất ra file {output_file}")
