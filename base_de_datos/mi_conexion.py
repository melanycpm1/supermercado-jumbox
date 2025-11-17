import sqlite3

class Connexion:
    def __init__(self, nombre_bd):
        self.conexion = sqlite3.connect(nombre_bd)
        self.cursor = self.conexion.cursor()

        #IMPORTANTE: activa las claves foráneas
        self.cursor.execute("PRAGMA foreign_keys = ON;")


    #                     TABLA SUCURSAL

    def crear_tabla_sucursal(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sucursal(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(50),
                direccion VARCHAR(100),
                telefono VARCHAR(30)
            )
        """)
        self.conexion.commit()
    
    def agregar_sucursal(self, nombre, direccion, telefono):
        self.cursor.execute("""
            INSERT INTO sucursal (nombre, direccion, telefono)
            VALUES (?, ?, ?)
        """, (nombre, direccion, telefono))
        self.conexion.commit()

    def editar_sucursal(self, id, nombre, direccion, telefono):
        self.cursor.execute("""
            UPDATE sucursal
            SET nombre=?, direccion=?, telefono=?
            WHERE id=?
        """, (nombre, direccion, telefono, id))
        self.conexion.commit()

    def eliminar_sucursal(self, id):
        self.cursor.execute("""
            DELETE FROM sucursal WHERE id=?
        """, (id,))
        self.conexion.commit()

    def mostrar_sucursales(self):
        self.cursor.execute("SELECT * FROM sucursal")
        return self.cursor.fetchall()

    #                     TABLA USUARIO

    def crear_tabla_usuario(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(40),
                apellido VARCHAR(40),
                email VARCHAR(100),
                contrasena VARCHAR(50),
                rol VARCHAR(50),
                sucursal_id INTEGER,
                FOREIGN KEY (sucursal_id) REFERENCES sucursal(id) ON DELETE CASCADE
            )
        """)
        self.conexion.commit()

    def agregar_usuario(self, nombre, apellido, email, contrasena, rol, sucursal_id):
        self.cursor.execute("""
            INSERT INTO usuario (nombre, apellido, email, contrasena, rol, sucursal_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, email, contrasena, rol, sucursal_id))
        self.conexion.commit()

    def editar_usuario(self, id, nombre, apellido, email, contrasena, rol, sucursal_id):
        self.cursor.execute("""
            UPDATE usuario
            SET nombre=?, apellido=?, email=?, contrasena=?, rol=?, sucursal_id=?
            WHERE id=?
        """, (nombre, apellido, email, contrasena, rol, sucursal_id, id))
        self.conexion.commit()

    def eliminar_usuario(self, id):
        self.cursor.execute("DELETE FROM usuario WHERE id=?", (id,))
        self.conexion.commit()

    def mostrar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuario")
        return self.cursor.fetchall()


    #                     TABLA PRODUCTO

    def crear_tabla_producto(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS producto(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(50),
                categoria VARCHAR(50),
                precio REAL,
                stock_minimo INTEGER
            )
        """)
        self.conexion.commit()

    def agregar_producto(self, nombre, categoria, precio, stock_minimo):
        self.cursor.execute("""
            INSERT INTO producto (nombre, categoria, precio, stock_minimo)
            VALUES (?, ?, ?, ?)
        """, (nombre, categoria, precio, stock_minimo))
        self.conexion.commit()

    def editar_producto(self, id, nombre, categoria, precio, stock_minimo):
        self.cursor.execute("""
            UPDATE producto
            SET nombre=?, categoria=?, precio=?, stock_minimo=?
            WHERE id=?
        """, (nombre, categoria, precio, stock_minimo, id))
        self.conexion.commit()

    def eliminar_producto(self, id):
        self.cursor.execute("DELETE FROM producto WHERE id=?", (id,))
        self.conexion.commit()


    #                     TABLA INVENTARIO

    def crear_tabla_inventario(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sucursal INTEGER,
                id_producto INTEGER,
                cantidad_actual INTEGER,
                FOREIGN KEY (id_sucursal) REFERENCES sucursal(id) ON DELETE CASCADE,
                FOREIGN KEY (id_producto) REFERENCES producto(id) ON DELETE CASCADE
            )
        """)
        self.conexion.commit()

    def agregar_inventario(self, id_sucursal, id_producto, cantidad_actual):
        self.cursor.execute("""
            INSERT INTO inventario (id_sucursal, id_producto, cantidad_actual)
            VALUES (?, ?, ?)
        """, (id_sucursal, id_producto, cantidad_actual))
        self.conexion.commit()

    def editar_inventario(self, id, id_sucursal, id_producto, cantidad_actual):
        self.cursor.execute("""
            UPDATE inventario
            SET id_sucursal=?, id_producto=?, cantidad_actual=?
            WHERE id=?
        """, (id_sucursal, id_producto, cantidad_actual, id))
        self.conexion.commit()

    def eliminar_inventario(self, id):
        self.cursor.execute("DELETE FROM inventario WHERE id=?", (id,))
        self.conexion.commit()

    def mostrar_inventario(self):
        self.cursor.execute("""
            SELECT i.id, s.nombre AS sucursal, p.nombre AS producto, i.cantidad_actual
            FROM inventario i
            JOIN sucursal s ON i.id_sucursal = s.id
            JOIN producto p ON i.id_producto = p.id
        """)
        return self.cursor.fetchall()


    #                      TABLA PEDIDO

    def crear_tabla_pedido(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedido(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sucursal_origen INTEGER,
                id_sucursal_destino INTEGER,
                fecha_pedido TEXT,
                estado TEXT,
                FOREIGN KEY (id_sucursal_origen) REFERENCES sucursal(id) ON DELETE CASCADE,
                FOREIGN KEY (id_sucursal_destino) REFERENCES sucursal(id) ON DELETE CASCADE
            )
        """)
        self.conexion.commit()

    def agregar_pedido(self, id_sucursal_origen, id_sucursal_destino, fecha_pedido, estado):
        self.cursor.execute("""
            INSERT INTO pedido (id_sucursal_origen, id_sucursal_destino, fecha_pedido, estado)
            VALUES (?, ?, ?, ?)
        """, (id_sucursal_origen, id_sucursal_destino, fecha_pedido, estado))
        self.conexion.commit()

    def editar_pedido(self, id, id_sucursal_origen, id_sucursal_destino, fecha_pedido, estado):
        self.cursor.execute("""
            UPDATE pedido
            SET id_sucursal_origen=?, id_sucursal_destino=?, fecha_pedido=?, estado=?
            WHERE id=?
        """, (id_sucursal_origen, id_sucursal_destino, fecha_pedido, estado, id))
        self.conexion.commit()

    def eliminar_pedido(self, id):
        self.cursor.execute("DELETE FROM pedido WHERE id=?", (id,))
        self.conexion.commit()

    def mostrar_pedidos(self):
        self.cursor.execute("""
            SELECT p.id, s1.nombre AS sucursal_origen, s2.nombre AS sucursal_destino,
                   p.fecha_pedido, p.estado
            FROM pedido p
            JOIN sucursal s1 ON p.id_sucursal_origen = s1.id
            JOIN sucursal s2 ON p.id_sucursal_destino = s2.id
        """)
        return self.cursor.fetchall()


    #                TABLA DETALLE PEDIDO

    def crear_tabla_detalle_pedido(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_pedido(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pedido INTEGER,
                id_producto INTEGER,
                cantidad_solicitada INTEGER,
                cantidad_enviada INTEGER,
                FOREIGN KEY (id_pedido) REFERENCES pedido(id) ON DELETE CASCADE,
                FOREIGN KEY (id_producto) REFERENCES producto(id) ON DELETE CASCADE
            )
        """)
        self.conexion.commit()

    def agregar_detalle_pedido(self, id_pedido, id_producto, cantidad_solicitada, cantidad_enviada):
        self.cursor.execute("""
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad_solicitada, cantidad_enviada)
            VALUES (?, ?, ?, ?)
        """, (id_pedido, id_producto, cantidad_solicitada, cantidad_enviada))
        self.conexion.commit()

    def editar_detalle_pedido(self, id, id_pedido, id_producto, cantidad_solicitada, cantidad_enviada):
        self.cursor.execute("""
            UPDATE detalle_pedido
            SET id_pedido=?, id_producto=?, cantidad_solicitada=?, cantidad_enviada=?
            WHERE id=?
        """, (id_pedido, id_producto, cantidad_solicitada, cantidad_enviada, id))
        self.conexion.commit()

    def eliminar_detalle_pedido(self, id):
        self.cursor.execute("DELETE FROM detalle_pedido WHERE id=?", (id,))
        self.conexion.commit()

    def mostrar_detalles_pedido(self):
        self.cursor.execute("""
            SELECT d.id, p.id AS pedido_id, pr.nombre AS producto,
                   d.cantidad_solicitada, d.cantidad_enviada
            FROM detalle_pedido d
            JOIN pedido p ON d.id_pedido = p.id
            JOIN producto pr ON d.id_producto = pr.id
        """)
        return self.cursor.fetchall()


    #                  TABLA NOTIFICACIÓN

    def crear_tabla_notificacion(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notificacion(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER,
                id_sucursal INTEGER,
                fecha TEXT,
                tipo TEXT,
                mensaje TEXT,
                FOREIGN KEY (id_producto) REFERENCES producto(id) ON DELETE CASCADE,
                FOREIGN KEY (id_sucursal) REFERENCES sucursal(id) ON DELETE CASCADE
            )
        """)
        self.conexion.commit()

    def agregar_notificacion(self, id_producto, id_sucursal, fecha, tipo, mensaje):
        self.cursor.execute("""
            INSERT INTO notificacion (id_producto, id_sucursal, fecha, tipo, mensaje)
            VALUES (?, ?, ?, ?, ?)
        """, (id_producto, id_sucursal, fecha, tipo, mensaje))
        self.conexion.commit()

    def editar_notificacion(self, id, id_producto, id_sucursal, fecha, tipo, mensaje):
        self.cursor.execute("""
            UPDATE notificacion
            SET id_producto=?, id_sucursal=?, fecha=?, tipo=?, mensaje=?
            WHERE id=?
        """, (id_producto, id_sucursal, fecha, tipo, mensaje, id))
        self.conexion.commit()

    def eliminar_notificacion(self, id):
        self.cursor.execute("DELETE FROM notificacion WHERE id=?", (id,))
        self.conexion.commit()

    def mostrar_notificaciones(self):
        self.cursor.execute("""
            SELECT n.id, p.nombre AS producto, s.nombre AS sucursal, 
                   n.fecha, n.tipo, n.mensaje
            FROM notificacion n
            JOIN producto p ON n.id_producto = p.id
            JOIN sucursal s ON n.id_sucursal = s.id
        """)
        return self.cursor.fetchall()


    #                        TABLA VENTA

    def crear_tabla_venta(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS venta(
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sucursal INTEGER,
                id_usuario INTEGER,
                fecha TEXT,
                total REAL,
                metodo_pago TEXT,
                estado TEXT,
                FOREIGN KEY (id_sucursal) REFERENCES sucursal(id) ON DELETE CASCADE,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
            )
        """)
        self.conexion.commit()
    
    def agregar_venta(self, id_sucursal, id_usuario, fecha, total, metodo_pago, estado):
        sql = """
            INSERT INTO venta (id_sucursal, id_usuario, fecha, total, metodo_pago, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (id_sucursal, id_usuario, fecha, total, metodo_pago, estado))
        self.conexion.commit()
        return self.cursor.lastrowid

    def editar_venta(self, id_venta, id_sucursal, id_usuario, fecha, total, metodo_pago, estado):
        sql = """
            UPDATE venta
            SET id_sucursal=?, id_usuario=?, fecha=?, total=?, metodo_pago=?, estado=?
            WHERE id_venta=?
        """
        self.cursor.execute(sql, (id_sucursal, id_usuario, fecha, total, metodo_pago, estado, id_venta))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar_venta(self, id_venta):
        sql = "DELETE FROM venta WHERE id_venta=?"
        self.cursor.execute(sql, (id_venta,))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def mostrar_ventas(self):
        self.cursor.execute("SELECT * FROM venta")
        return self.cursor.fetchall()


    #                 TABLA DETALLE VENTA

    def crear_tabla_detalle_venta(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_venta(
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER,
                id_producto INTEGER,
                cantidad INTEGER,
                precio_unit REAL,
                subtotal REAL,
                FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE,
                FOREIGN KEY (id_producto) REFERENCES producto(id) ON DELETE CASCADE
            )
        """)
        self.conexion.commit()

    def agregar_detalle_venta(self, id_venta, id_producto, cantidad, precio_unit, subtotal):
        self.cursor.execute("""
            INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unit, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (id_venta, id_producto, cantidad, precio_unit, subtotal))
        self.conexion.commit()
        return self.cursor.lastrowid

    def editar_detalle_venta(self, id_detalle, id_producto, cantidad, precio_unit, subtotal):
        self.cursor.execute("""
            UPDATE detalle_venta
            SET id_producto=?, cantidad=?, precio_unit=?, subtotal=?
            WHERE id_detalle=?
        """, (id_producto, cantidad, precio_unit, subtotal, id_detalle))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar_detalle_venta(self, id_detalle):
        self.cursor.execute("DELETE FROM detalle_venta WHERE id_detalle=?", (id_detalle,))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def mostrar_detalles_venta(self, id_venta):
        self.cursor.execute("""
            SELECT * FROM detalle_venta WHERE id_venta=?
        """, (id_venta,))
        return self.cursor.fetchall()

    #             MÉTODOS DE ELIMINACIÓN RÁPIDA
    def eliminar_todo_inventario(self):
        self.cursor.execute("DELETE FROM inventario")
        self.conexion.commit()

    def eliminar_todo_producto(self):
        self.cursor.execute("DELETE FROM producto")
        self.conexion.commit()

    def eliminar_producto_y_inventario(self, id):
        self.cursor.execute("DELETE FROM inventario WHERE id_producto=?", (id,))
        self.cursor.execute("DELETE FROM producto WHERE id=?", (id,))
        self.conexion.commit()
    

    #               CERRAR LA BASE DE DATOS

    def cerrar(self):
        self.conexion.close()