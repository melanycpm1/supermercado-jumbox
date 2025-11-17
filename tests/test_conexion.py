import unittest
from base_de_datos.mi_conexion import Connexion
from datetime import datetime

class TestConnexion(unittest.TestCase):

    def setUp(self):
        # Base de datos temporal en memoria
        self.db = Connexion(":memory:")

        # Crear TODAS las tablas
        self.db.crear_tabla_sucursal()
        self.db.crear_tabla_usuario()
        self.db.crear_tabla_producto()
        self.db.crear_tabla_inventario()
        self.db.crear_tabla_pedido()
        self.db.crear_tabla_detalle_pedido()
        self.db.crear_tabla_notificacion()
        self.db.crear_tabla_venta()
        self.db.crear_tabla_detalle_venta()


    
    # TEST TABLA SUCURSAL
    def test_agregar_sucursal(self):
        self.db.agregar_sucursal("Sucursal X", "Calle Falsa 123", "1111")
        fila = self.db.cursor.execute("SELECT * FROM sucursal").fetchone()
        self.assertIsNotNone(fila)
        self.assertEqual(fila[1], "Sucursal X")


    # TEST TABLA USUARIO
    def test_agregar_usuario(self):
        self.db.agregar_sucursal("Sucursal X", "Calle Falsa 123", "1111")
        self.db.agregar_usuario("Ana", "Lopez", "ana@x", "1234", "admin", 1)

        fila = self.db.cursor.execute(
            "SELECT nombre, apellido, email FROM usuario WHERE email='ana@x'"
        ).fetchone()

        self.assertIsNotNone(fila)
        self.assertEqual(fila[0], "Ana")
        self.assertEqual(fila[1], "Lopez")

    # TEST TABLA PRODUCTO
    def test_agregar_producto(self):
        self.db.agregar_producto("Manzana", "Fruta", 100.5, 10)
        fila = self.db.cursor.execute("SELECT nombre, categoria FROM producto").fetchone()

        self.assertEqual(fila[0], "Manzana")
        self.assertEqual(fila[1], "Fruta")


    # TEST TABLA INVENTARIO
    def test_agregar_inventario(self):
        self.db.agregar_sucursal("A", "B", "C")
        self.db.agregar_producto("P1", "Cat", 100, 5)

        self.db.agregar_inventario(1, 1, 50)
        fila = self.db.cursor.execute("SELECT cantidad_actual FROM inventario").fetchone()

        self.assertEqual(fila[0], 50)


    # TEST TABLA PEDIDO
    def test_agregar_pedido(self):
        self.db.agregar_sucursal("A", "B", "C")
        self.db.agregar_sucursal("A2", "B2", "C2")

        self.db.agregar_pedido(1, 2, "2024-01-01", "pendiente")

        fila = self.db.cursor.execute("SELECT estado FROM pedido").fetchone()
        self.assertEqual(fila[0], "pendiente")


    # TEST DETALLE PEDIDO
    def test_detalle_pedido(self):
        self.db.agregar_sucursal("A", "B", "C")
        self.db.agregar_sucursal("A2", "B2", "C2")
        self.db.agregar_producto("Prod", "Cat", 123, 1)

        self.db.agregar_pedido(1, 2, "2024-01-01", "pendiente")
        self.db.agregar_detalle_pedido(1, 1, 5, 5)

        fila = self.db.cursor.execute(
            "SELECT cantidad_solicitada FROM detalle_pedido"
        ).fetchone()

        self.assertEqual(fila[0], 5)


    # TEST NOTIFICACIÓN
    def test_notificacion(self):
        self.db.agregar_sucursal("A", "B", "C")
        self.db.agregar_producto("Prod", "Cat", 10, 2)

        self.db.agregar_notificacion(1, 1, "2024-01-01", "alerta", "Mensaje")

        fila = self.db.cursor.execute("SELECT tipo FROM notificacion").fetchone()
        self.assertEqual(fila[0], "alerta")


    # TEST VENTA Y DETALLE VENTA
    def test_venta_y_detalle(self):
        self.db.agregar_sucursal("Suc", "Dir", "Tel")
        self.db.agregar_usuario("Ana", "L", "ana@x", "1234", "vendedor", 1)
        self.db.agregar_producto("Prod", "Cat", 10, 1)

        id_venta = self.db.agregar_venta(1, 1, "2024-01-01", 100.0, "efectivo", "completado")
        self.assertTrue(id_venta > 0)

        id_det = self.db.agregar_detalle_venta(id_venta, 1, 2, 10, 20)
        self.assertTrue(id_det > 0)

        detalles = self.db.mostrar_detalles_venta(id_venta)
        self.assertEqual(len(detalles), 1)
        self.assertEqual(detalles[0][3], 2)  # cantidad


if __name__ == "__main__":
    unittest.main()