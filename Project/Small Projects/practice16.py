import numpy as np

# arr = np.arange(1,21)
# print("Tổng là", np.sum(arr))
# print("Trung bình là ", np.mean(arr))
# print("Giá trị lớn nhất là ", np.max(arr))
# print("Các phần tử chia hết cho 3 ", arr[arr%3 ==0])
#
# matrix = np.random.randint(1,100,(3,3))
# print("Ma trận ", matrix)
# print(np.sum(matrix, axis=1))
# print(np.sum(matrix, axis=0))
# print(np.trace(matrix))

import pandas as pd

# data = {
#     "Name": ["Alice", "Bob", "Charlie", "David"],
#     "Age": [18, 25 , 28, 31],
#     "Department": ["HR", "IT", "Finance", "IT"],
#     "Salary": [5000, 7000, 8000, 6000]
# }
#
# df = pd.DataFrame(data)
# df["Bouns"] = df["Salary"]*0.1
# high_slary = df[df["Salary"]>7000]
# print(high_slary)

# data = {
#     "Name": ["Alice", "Bob", "Charlie", "David"],
#     "Age": [25, np.nan, 35, 40],
#     "Salary": [5000, 7000, np.nan, 6000]
# }
# df = pd.DataFrame(data)
# print("Số giá trị NaN mỗi cột:\n", df.isnull().sum())
# df.fillna(0, inplace=True)
# print("Dữ liệu sau khi thay thế NaN:\n", df)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df = pd.read_csv("C:\\Users\\h\\Downloads\\sales_data.csv")
#
# df = df.dropna()  # Loại bỏ tất cả các dòng có giá trị NaN
# print(df.head())
# print(df.info())
# df["revenue"].fillna(df["quantity"]*df["price"])
# df["price"].fillna(df["price"].median())
# df.drop_duplicates(inplace=True)
# df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
# df["month"] = df["date"].dt.to_period("M")
# monthly_revenue = df.groupby("month")["revenue"].sum()
# print(monthly_revenue)
#
# top_products = df.groupby("product")["quantity"].sum().nlargest(5)
# print(top_products)
#
# # plt.figure(figsize=(10, 5))
# # monthly_revenue.plot(kind="line", marker="o", color="b")
# # plt.title("Doanh thu theo tháng")
# # plt.xlabel("Tháng")
# # plt.ylabel("Doanh thu")
# # plt.grid(True)
# # plt.show()
# df = df[df["revenue"]>0]                       ,
# print(df.info())  # Xem lại số lượng dòng và cột
#
# df.to_parquet("sales_cleaned.parquet", index=False)
# data = pd.read_parquet("sales_cleaned.parquet")
# print(data)

# df = pd.read_csv("C:\\Users\\h\\Downloads\\sales_data (1).csv")
# print(df.info())
# print(df.describe())
# df["revenue"]=df["revenue"].fillna(df["quantity"]*df["price"])
# df = df.dropna()
# df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
# df["month"] = df["date"].dt.to_period("M")
# product_revenue = df.groupby("product")["revenue"].sum()
# average_product = df.groupby("product")["quantity"].mean()
# df_sorted = df.sort_values("revenue", ascending=False)
#
# df.to_csv("cleaned_sales_data.csv")

# df = pd.read_csv("C:\\Users\\h\\Downloads\\advanced_sales_data.csv")
# # print(df.info())
# df["revenue"] = df["revenue"].fillna(df["quantity"]*df["price"])
# df["region"] = df["region"].fillna("Unknown")
# df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
# df["month"] = df["date"].dt.to_period("M")
# order_numbers = df.groupby("customer_id")["order_id"].count()
# df["customer_type"] = df["customer_id"].map(lambda x: "Loyal" if order_numbers[x] > 2 else "New")
#
# print(df)


