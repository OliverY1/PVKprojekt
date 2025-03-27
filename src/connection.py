import psycopg2
import details as d

conn = psycopg2.connect(
    host=d.host,
    database=d.database,
    user=d.user,
    password=d.password
)

cursor = conn.cursor()