import psycopg2

conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Lấy danh sách cơ sở dữ liệu
cur.execute("SELECT datname FROM pg_database;")
databases = cur.fetchall()

# In danh sách cơ sở dữ liệu
for db in databases:
    print(db[0])

cur.close()
conn.close()
