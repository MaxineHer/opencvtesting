import pymysql

try:
    connection = pymysql.connect(
        host="192.168.0.131",
        user="root",
        password="password",
        database="fridgefinds",
        charset='utf8mb4',
    )
    print("MySQL connection successful!")
    connection.close()

except pymysql.err.OperationalError as e:
    print(f"MySQL connection failed: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")