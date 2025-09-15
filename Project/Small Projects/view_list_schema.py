import psycopg2

conn = psycopg2.connect(
    dbname="mspeedy",
    user="mspeedy",
    password="mspeedy",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Lấy danh sách schema
cur.execute("SELECT nspname FROM pg_catalog.pg_namespace;")
schemas = cur.fetchall()

# In danh sách schema
for schema in schemas:
    print(schema[0])

cur.close()
conn.close()
