import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="sports_team",
        user="postgres",
        password="Mukul@1997",
        port="5432"
    )
    print("PostgreSQL connected successfully")
    conn.close()

except Exception as e:
    print("Connection failed")
    print(e)

