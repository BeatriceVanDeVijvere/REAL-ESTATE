import psycopg2

def get_container_ip():
    # Run a command in the container to get the IP address
    conn = psycopg2.connect(
        host="localhost",
        database="realestate",
        user="postgres",
        password="bea"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pg_catalog.pg_tables")
    rows = cursor.fetchall()
    container_ip = rows[0][1]
    cursor.close()
    conn.close()
    return container_ip

