from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, month

# Tạo SparkSession
spark = SparkSession.builder.appName("Sales Analysis").getOrCreate()

# Đọc file CSV
file_path = "C:\\Users\\h\\Downloads\\large_sales_data.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

df = df.withColumn("revenue", col("quantity")*col("price"))
revenue_by_region = df.groupby("region").agg(_sum("revenue").alias("total_revenue"))
revenue_by_region.show()

revenue_by_customer = df.groupby("customer_name").agg(_sum("revenue").alias("total_revenue"))
top_customer = revenue_by_customer.orderBy(col("total_revenue").desc()).limit(1)
top_customer.show()

