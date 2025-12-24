def execute_query(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)

        columns = [col[0] for col in cur.description]
        rows = cur.fetchall()
        return columns, rows

    finally:
        pass  # Không close conn ở đây, vì sẽ tái sử dụng
