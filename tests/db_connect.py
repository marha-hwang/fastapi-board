import pymysql

try:
    connection = pymysql.connect(
        host='localhost',  # 또는 실제 호스트
        port=3306,
        user='haram',
        password='1111',
        database='board',
        charset='utf8mb4'
    )
    print("연결 성공!")
    connection.close()
except Exception as e:
    print(f"연결 실패: {e}")