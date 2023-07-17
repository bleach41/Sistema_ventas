import sqlite3
from sqlite3 import Error


class QueriesSQLite:

    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    def execute_query(connection, query, data_tuple):
        cursor = connection.cursor()
        try:
            cursor.execute(query, data_tuple)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")


if __name__ == "__main__":
    connection = QueriesSQLite.create_connection(
        "ventas/db_ventas/inventario.sqlite")

    # create_product_table = """CREATE TABLE IF NOT EXISTS productos(
    #                             id TEXT PRIMARY KEY,
    #                             nombre TEXT NOT NULL,
    #                             precio REAL NOT NULL,
    #                             cantidad INTEGER NOT NULL
    #                             );
    #                         """
    # QueriesSQLite.execute_query(connection, create_product_table, tuple())

    # create_user_table = """
    #                         CREATE TABLE IF NOT EXISTS usuarios(
    #                         username TEXT PRIMARY KEY,
    #                         nombre TEXT NOT NULL,
    #                         password TEXT NOT NULL,
    #                         tipo TEXT NOT NULL
    #                         );
    #                     """
    # QueriesSQLite.execute_query(connection, create_user_table, tuple())

    # crear_producto = """
    #                     INSERT INTO
    #                     productos (id, nombre, precio, cantidad)
    #                     VALUES
    #                         ('111', 'leche 1l', 20, 20),
    #                         ('222', 'cereal 500g', 50, 15),
    #                         ('333', 'yogurt 1L', 25, 10),
    #                         ('444', 'helado 2L', 80, 20),
    #                         ('555', 'alimento para perro 20kg', 750, 5),
    #                         ('666', 'shampoo', 100, 25),
    #                         ('777', 'papel higiénico 4 rollos', 35, 30),
    #                         ('888', 'jabón para trastes', 65, 5)
    #                 """
    # QueriesSQLite.execute_query(connection, crear_producto, tuple())

    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)

    # usuario_tuple = ('persona1', 'Persona 1', 'abc', 'admin')
    # crear_usuario = """
    # INSERT INTO
    #   usuarios (username, nombre, password, tipo)
    # VALUES
    #     (?,?,?,?);
    # """
    # QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:", usuario)

    # nueva_data = ('Persona 55', '123', 'admin', 'persona1')
    # actualizar = """UPDATE usuarios SET nombre=?, password=?, tipo = ? WHERE username = ? """
    # QueriesSQLite.execute_query(connection, actualizar, nueva_data)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:", usuario)

    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)

    select_users = "SELECT * from usuarios"
    usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    for usuario in usuarios:
        print("type:", type(usuario), "usuario:", usuario)

    # producto_a_borrar = ('888',)
    # borrar = """DELETE from productos where id = ?"""
    # QueriesSQLite.execute_query(connection, borrar, producto_a_borrar)

    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)

    # connection.close()
