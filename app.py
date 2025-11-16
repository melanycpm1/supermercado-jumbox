from flask import Flask;
from base_de_datos.mi_conexion import Connexion
import os

app = Flask(__name__)
app.secret_key = "clave_super_segura"

DB_NAME = "database.db"
db = Connexion(DB_NAME)

if not os.path.exists(DB_NAME):
    print("Creando base de datos por primera vez...")
    db = Connexion(DB_NAME)

    # Crear tablas
    db.crear_tabla_sucursal()
    db.crear_tabla_usuario()
    db.crear_tabla_producto()
    db.crear_tabla_inventario()
    db.crear_tabla_pedido()
    db.crear_tabla_detalle_pedido()
    db.crear_tabla_notificacion()
    db.crear_tabla_venta()  
    db.crear_tabla_detalle_venta()
else:
    # Si ya existe, simplemente conecta
    db = Connexion(DB_NAME)

