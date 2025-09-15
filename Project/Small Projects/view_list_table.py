import psycopg2

conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Kiểm tra bảng trong schema public
cur.execute("SELECT tablename FROM pg_catalog.pg_tables where schemaname = 'mst_data' or schemaname = 'msx_data' ;")
tables = cur.fetchall()

# In danh sách bảng
if tables:
    for table in tables:
        print(table[0])
else:
    print("No tables found in the public schema.")

cur.close()
conn.close()
