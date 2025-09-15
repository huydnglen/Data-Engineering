import pandas as pd

df = pd.read_csv("F:\pythonProject2\web_data.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
average_time_page = df.groupby("Page")["Duration (s)"].mean()
total_time_page = df.groupby("Page")["Duration (s)"].sum()
time_user = df.groupby("User ID")["Duration (s)"].sum()
most_time_user = time_user.idxmax()
most_time = time_user.max()
# Tạo cột 'Date' từ 'Timestamp'
df["Date"] = df["Timestamp"].dt.date
# Tính số lượt truy cập mỗi ngày
daily_visits = df.groupby("Date").size()
print(df["Date"])
print(daily_visits)