from django.db import connection
from contextlib import closing


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


"""table_name.objects.all() orniga bundan foydalandim"""
def get_data_from_table(table_name):
    # connection.cursor() yordamida bazaga  ulanamiz va cursor obyektini ochamiz
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        return dictfetchall(cursor)


def get_table():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
            SELECT users_orderproduct.product_id, users_product.title,
            COUNT(users_orderproduct.product_id) AS count
            FROM users_orderproduct
            INNER JOIN  users_product ON users_orderproduct.product_id = users_product.id
            GROUP BY users_orderproduct.product_id, users_product.title
            ORDER BY count DESC LIMIT 5
        """)
        table = dictfetchall(cursor)
        return table


def get_order_by_user(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
            SELECT users_customer.first_name, users_customer.last_name, users_order.id, users_order.address, users_order.payment_type, users_order.status, users_order.created_at
            FROM users_order
            INNER JOIN users_customer ON users_customer.id = users_order.customer_id
            WHERE users_order.customer_id = %s
        """, [id])
        order = dictfetchall(cursor)
        return order


def get_product_by_order(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT users_orderproduct.count,users_orderproduct.price,users_orderproduct.created_at,users_product.title 
                           FROM users_orderproduct 
                           INNER JOIN users_product ON users_orderproduct.product_id=users_product.id  WHERE order_id=%s""", [id])
        orderproduct = dictfetchall(cursor)
        return orderproduct
