# Đề bài cụ thể cho dự án ETL: Hệ thống phân tích doanh thu công ty bán lẻ
# Mục tiêu:
# Công ty bán lẻ muốn xây dựng một hệ thống tự động phân tích dữ liệu doanh thu từ nhiều nguồn và tạo báo cáo hàng tuần. Dữ liệu đến từ:
#
# File CSV: Giao dịch hàng ngày (do nhân viên nhập liệu).
# API: Thông tin khuyến mãi từng sản phẩm (cập nhật liên tục từ hệ thống marketing).
# Database: Thông tin khách hàng (PostgreSQL).
# Công ty cần báo cáo:
#
# Tổng doanh thu theo ngày và tháng.
# Sản phẩm bán chạy nhất mỗi tuần.
# Phân tích doanh thu theo khu vực và loại khách hàng.

import pandas as pd
import psycopg2
from  sqlalchemy import create_engine

#đọc file csv
transaction_data = pd.read_csv('F:\\pythonProject2\\transactions.csv')
print(transaction_data)

promote_data = pd.read_json('F:\\pythonProject2\\promotes.json')
print(promote_data)

engine = create_engine("postgresql://postgres:Congchua812%40@localhost:5432/retail_db")
customer = pd.read_sql("SELECT * FROM customer", con=engine)
print(customer)

transactions = transaction_data.merge(promote_data, on="product_id", how="left")
transactions = transactions.merge(customer, on="customer_id", how="left")
print(transactions)

transactions['discounted_price'] = transactions['price']*(1 - transactions['discount'])
transactions['total_revenue'] = transactions['quantity']*transactions['discounted_price']

#tổng doanh thu theo ngày
revenue_by_day = transactions.groupby('transaction_date')['total_revenue'].sum()
print(revenue_by_day)

#tổng doanh thu theo tháng
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date']).dt.to_period('M').astype(str)
revenue_by_month = transactions.groupby('transaction_date')['total_revenue'].sum()
print(revenue_by_month)

#lưu vào sql
transactions.to_sql("processed_transactions", con=engine, if_exists="replace", index=False)

#xuất excel
with pd.ExcelWriter("retail_report.xlsx") as writer:
    revenue_by_day.to_excel(writer, sheet_name="revenue by day")