from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg, to_date, month, year

# 1. Tạo SparkSession
spark = SparkSession.builder \
    .appName("Retail Analysis") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()

# 2. Đọc dữ liệu
transactions = spark.read.csv("C:\\Users\\h\\Downloads\\transactions_large.csv", header=True, inferSchema=True)
products = spark.read.json("C:\\Users\\h\\Downloads\\products_extended.json", multiLine=True)
stores = spark.read.csv("C:\\Users\\h\\Downloads\\stores.csv", header=True, inferSchema=True)
# Đổi tên cột price trong products
products = products.withColumnRenamed("price", "product_price")

# Thực hiện join
transactions = transactions.join(products, on="product_id", how="left")

# 3. Xử lý và kết hợp dữ liệu
transactions = transactions.join(products, on="product_id", how="left")
transactions = transactions.join(stores, on="store_id", how="left")

# 4. Tính tổng doanh thu theo thời gian
transactions = transactions.withColumn("transaction_date", to_date(col("transaction_date")))
monthly_revenue = transactions.groupBy(year("transaction_date").alias("year"),
                                       month("transaction_date").alias("month")) \
                               .agg(sum(col("price") * col("quantity")).alias("total_revenue"))

# 5. Phân tích doanh thu theo khu vực
region_revenue = transactions.groupBy("region").agg(
    sum(col("price") * col("quantity")).alias("total_revenue"),
    count("*").alias("transaction_count")
)

# 6. Dự đoán doanh thu (mẫu với pyspark.ml)
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

# Chuẩn bị dữ liệu
assembler = VectorAssembler(inputCols=["year", "month"], outputCol="features")
train_data = assembler.transform(monthly_revenue).select("features", "total_revenue")

# Huấn luyện mô hình
lr = LinearRegression(featuresCol="features", labelCol="total_revenue")
model = lr.fit(train_data)

# Dự đoán doanh thu
predictions = model.transform(train_data)

# 7. Lưu kết quả
monthly_revenue.write.csv("monthly_revenue.csv", header=True)
region_revenue.write.csv("region_revenue.csv", header=True)
