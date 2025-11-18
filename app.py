from flask import Flask,render_template,session,url_for, redirect,request;
import json
from base_de_datos.mi_conexion import Connexion
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_super_segura"

DB_NAME = "database.db"
db = Connexion(DB_NAME)

# Detectar si la base está vacía (sin tablas)
def base_de_datos_vacia():
    tablas = db.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()    
    return len(tablas) == 0

if base_de_datos_vacia():
    print("Creando tablas e insertando datos...")

    db.crear_tabla_sucursal()
    db.crear_tabla_usuario()
    db.crear_tabla_producto()
    db.crear_tabla_inventario()
    db.crear_tabla_pedido()
    db.crear_tabla_detalle_pedido()
    db.crear_tabla_notificacion()
    db.crear_tabla_venta()
    db.crear_tabla_detalle_venta()

    db.agregar_sucursal("Sucursal Central", "Av. Siempre Viva 123", "123456789")
    db.agregar_sucursal("Sucursal Norte", "Calle Los Álamos 456", "987654321")
    db.agregar_sucursal("Sucursal Sur", "Av. del Libertador 890", "1122334455")
    db.agregar_sucursal("Sucursal Este", "Calle Las Rosas 234", "2233445566")
    db.agregar_sucursal("Sucursal Oeste", "Boulevard San Martín 765", "3344556677")

    db.agregar_usuario("Juan", "Pérez", "admi@correo.com", "1234", "admi", 1)
    db.agregar_usuario("Carla", "Rodríguez", "carla.encargada@correo.com", "1234", "encargado", 1)
    db.agregar_usuario("Lucas", "Martínez", "lucas.reponedor@correo.com", "1234", "reponedor", 1)
    db.agregar_usuario("matias", "Martínez", "matias.vendedor@correo.com", "1234", "vendedor", 1)
else:
    print("Base de datos existente — no se crean tablas.")


@app.route("/")
def login():
    return render_template("login.html") #puede ingresar cualquiera

@app.route("/panel_principal")#puede ingresar cualquiera
def panel_principal():
    if "rol" not in session:
        return redirect(url_for("login"))  # si no está logueado
    
    return render_template("panel_principal.html",usuarioNombre=session["nombre"], usuarioApellido=session["apellido"], usuarioRol=session["rol"])

@app.route("/gestion_inventario")
def gestion_inventario():
    if "rol" not in session:
        return redirect(url_for("login"))  # si no está logueado
    
    if session["rol"] == "vendedor":
        return "Acceso denegado. No tenés permisos para entrar acá.", 403 #solo ingresaran los usuarios administradores,encargado,reponedor
    
    id_sucursal = session.get("sucursal_id")
    if not id_sucursal:
        db.conexion.close()
        return redirect(url_for("home"))
    db = Connexion("database.db")
    db.cursor.execute("""
    SELECT producto.nombre,
            producto.categoria,
            producto.precio,
            producto.stock_minimo,
            inventario.cantidad_actual,
            producto.id
    FROM producto
    INNER JOIN inventario ON producto.id = inventario.id_producto
    WHERE inventario.id_sucursal = ?
""", (id_sucursal,))
    
    productos = db.cursor.fetchall()
    print("Productos encontrados:", productos) 


    
    return render_template("inventario.html",
                            usuarioNombre=session["nombre"], 
                            usuarioApellido=session["apellido"], 
                            usuarioRol=session["rol"],
                            productos=productos)




@app.route("/gestion_pedidos")
def gestion_pedidos():
    rol = session["rol"]
    id_sucursal =  session["sucursal_id"]

    if rol == "encargado":
        # pedidos generados por mi sucursal
        pedidos_generados = db.cursor.execute("""
            SELECT p.id, s1.nombre, s2.nombre, p.fecha_pedido, p.estado
            FROM pedido p
            JOIN sucursal s1 ON p.id_sucursal_origen = s1.id
            JOIN sucursal s2 ON p.id_sucursal_destino = s2.id
            WHERE p.id_sucursal_origen = ?
        """, (id_sucursal,)).fetchall()

        # pedidos recibidos por mi sucursal
        pedidos_recibidos = db.cursor.execute("""
            SELECT p.id, s1.nombre, s2.nombre, p.fecha_pedido, p.estado
            FROM pedido p
            JOIN sucursal s1 ON p.id_sucursal_origen = s1.id
            JOIN sucursal s2 ON p.id_sucursal_destino = s2.id
            WHERE p.id_sucursal_destino = ?
        """, (id_sucursal,)).fetchall()

        productos_bajos = db.productos_stock_bajo(id_sucursal)

    elif rol == "admi":
        pedidos_generados = db.mostrar_pedidos()
        pedidos_recibidos = pedidos_generados
        productos_bajos = []

    else:
        return "No autorizado", 403

    sucursales = db.cursor.execute("SELECT id, nombre FROM sucursal").fetchall()

    return render_template(
        "pedidos.html",
        suarioNombre=session["nombre"], 
        usuarioApellido=session["apellido"], 
        usuarioRol=session["rol"],
        rol=rol,
        pedidos_generados=pedidos_generados,
        pedidos_recibidos=pedidos_recibidos,
        productos_bajos=productos_bajos,
        sucursales=sucursales
    )

@app.route("/gestion_usuarios")
def gestion_usuario():
    if "rol" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admi":
        return "Acceso denegado.", 403

    # Conexión local dentro de la función
    db = Connexion("database.db")  
    usuarios = db.mostrar_usuarios()
    sucursales = db.mostrar_sucursales()
    db.conexion.close()  # cerrar al final

    return render_template("usuarios.html",
                            usuarioNombre=session["nombre"],
                            usuarioApellido=session["apellido"],
                            usuarioRol=session["rol"],
                            usuarios=usuarios,
                            sucursales=sucursales)

@app.route("/reportes")
def reportes():
    if "rol" not in session:
        return redirect(url_for("login"))  # si no está logueado
    
    if session["rol"] == "reponedor" or session["rol"] == "vendedor":
        return "Acceso denegado. No tenés permisos para entrar acá.", 403


    return  #agregar tamblate

#@app.route("/notificaciones")
#def notificaciones():
    #  if "rol" not in session:
    #     return redirect(url_for("login"))  # si no está logueado
        
    # return render_template

@app.route("/ventas")
def ventas():

    if "rol" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "vendedor":
        return "Acceso denegado. No tenés permisos para entrar acá.", 403

    # PRIMERO OBTENGO LA SUCURSAL DEL VENDEDOR
    id_sucursal = session["sucursal_id"]

    conexion = Connexion("database.db")
    conexion.cursor.execute("SELECT nombre FROM sucursal WHERE id = ?", (id_sucursal,))
    nombre_sucursal = conexion.cursor.fetchone()[0]

    productos = db.mostrar_productos_con_stock(id_sucursal)

    vendedor_nombre = f"{session['nombre']} {session['apellido']}"

    conexion.conexion.close()

    return render_template(
        "ventas.html",
        usuarioNombre=session["nombre"],
        usuarioApellido=session["apellido"],
        usuarioRol=session["rol"],
        id_sucursal=id_sucursal,
        nombre_sucursal=nombre_sucursal,
        productos=productos,
        vendedor=vendedor_nombre
    )


####

@app.route("/inicio_sesion", methods=["POST"])
def mostrar_login():
    email = request.form["email"]
    password = request.form["password"]

    conexion = Connexion("database.db")
    conexion.cursor.execute(
        "SELECT * FROM usuario WHERE email = ? AND contrasena = ?", (email, password)
    )
    usuario = conexion.cursor.fetchone()
    conexion.conexion.close()

    if usuario:
        session["usuario_id"] = usuario[0]
        session["nombre"] = usuario[1]
        session["apellido"] = usuario[2]
        session["rol"] = usuario[5]
        session["sucursal_id"] = usuario[6]

        return redirect(url_for("panel_principal"))
    else:
        return "Email o contraseña incorrectos"
    

@app.route("/agregar_producto", methods=["POST"])
def agregar_producto():
    if "rol" not in session:
        return redirect(url_for("home"))

    id_sucursal = session.get("sucursal_id")
    if not id_sucursal:
        return redirect(url_for("home"))

    #Obtener datos del formulario 
    nombre = request.form["nombre_producto"]
    categoria = request.form["categoria"]
    precio = request.form["precio"]
    stock_minimo = request.form["stock_minimo"]
    cantidad_actual = request.form["cantidad_actual"]

    # Guardar en la base 
    db = Connexion("database.db")
    db.agregar_producto(nombre, categoria, precio, stock_minimo)

    # Obtener el id del último producto insertado
    id_producto = db.cursor.lastrowid

    # Agregarlo al inventario de esa sucursal
    db.agregar_inventario(id_sucursal, id_producto, cantidad_actual)

    db.conexion.close()

    # Volver a la página principal del inventario
    return redirect(url_for("gestion_inventario"))
    
@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    id_producto = request.form["id_producto"]
    db = Connexion("database.db")
    db.eliminar_producto_y_inventario(id_producto)
    db.cerrar()
    return redirect(url_for("gestion_inventario"))

@app.route("/actualizar_inventario", methods=["POST"])
def actualizar_inventario():
    id_producto = request.form.get("id_producto")
    nueva_cantidad = int(request.form.get("cantidad_actual"))
    cantidad_actual = int(request.form.get("cantidad_previa"))  # vas a enviar este dato también

    #No permitir que se reduzca la cantidad
    if nueva_cantidad < cantidad_actual:
        return "No podés cargar una cantidad menor a la actual", 400

    db = Connexion("database.db")
    db.cursor.execute("""
        UPDATE inventario 
        SET cantidad_actual = ?
        WHERE id_producto = ?
    """, (nueva_cantidad, id_producto))
    db.conexion.commit()

    return redirect(url_for("gestion_inventario"))

@app.route("/editar_producto", methods=["POST"])
def editar_producto():
    id_producto = request.form["id"]
    nombre = request.form["nombre"]
    categoria = request.form["categoria"]
    precio = request.form["precio"]
    stock_minimo = request.form["stock_minimo"]

    db = Connexion("database.db")

    db.cursor.execute("""
        UPDATE producto
        SET nombre = ?, categoria = ?, precio = ?, stock_minimo = ?
        WHERE id = ?
    """, (nombre, categoria, precio, stock_minimo, id_producto))

    db.conexion.commit()
    db.conexion.close()

    return redirect(url_for("gestion_inventario"))

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    contrasena = request.form['contrasena']
    rol = request.form['rol']
    sucursal_id = request.form['sucursal_id']

    # Crear conexión local dentro de la función
    db_local = Connexion("database.db")
    db_local.agregar_usuario(nombre, apellido, email, contrasena, rol, sucursal_id)
    db_local.conexion.close()  

    return redirect(url_for('gestion_usuario'))

@app.route("/editar_usuario/<int:id>", methods=["POST"])
def editar_usuario(id):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    contrasena = request.form["contrasena"]  
    rol = request.form["rol"]
    sucursal_id = request.form["sucursal_id"]

    # # Crear conexión local dentro de la función para evitar errores
    db_local = Connexion("database.db")

    if contrasena == "":
        # No actualizar contraseña
        db_local.cursor.execute("""
            UPDATE usuario 
            SET nombre=?, apellido=?, email=?, rol=?, sucursal_id=?
            WHERE id=?
        """, (nombre, apellido, email, rol, sucursal_id, id))

    else:
        # Actualizar con contraseña 
        db_local.cursor.execute("""
            UPDATE usuario 
            SET nombre=?, apellido=?, email=?, contrasena=?, rol=?, sucursal_id=?
            WHERE id=?
        """, (nombre, apellido, email, contrasena, rol, sucursal_id, id))

    db_local.conexion.commit()
    db_local.conexion.close()

    return redirect(url_for("gestion_usuario"))


@app.route("/registrar_venta", methods=["POST"])
def registrar_venta():
    id_sucursal = request.form["id_sucursal"]
    id_usuario = request.form["id_usuario"]
    fecha = request.form["fecha"]
    metodo = request.form["metodo_pago"]
    estado = request.form["estado"]

    detalle_json = json.loads(request.form["detalle_json"])

    # calcular total desde el detalle
    total = sum(item["subtotal"] for item in detalle_json)

    # crear venta
    id_venta = db.agregar_venta(id_sucursal, id_usuario, fecha, total, metodo, estado)

    # insertar cada detalle y actualizar stock
    for item in detalle_json:
        db.agregar_detalle_venta(
            id_venta,
            item["id_producto"],
            item["cantidad"],
            item["precio_unit"],
            item["subtotal"]
        )

        # RESTAR STOCK
        db.cursor.execute("""
    UPDATE inventario
    SET cantidad_actual = cantidad_actual - ?
    WHERE id_producto = ? AND id_sucursal = ?
""", (item["cantidad"], item["id_producto"], id_sucursal))

        db.conexion.commit()

    return redirect("/ventas")


@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    db_local = Connexion("database.db")  
    db_local.eliminar_usuario(id)
    db_local.conexion.close()  
    return redirect(url_for('gestion_usuario'))

@app.route("/generar_pedido", methods=["POST"])
def generar_pedido():
    if session["rol"] != "encargado":
        return "No autorizado", 403

    id_sucursal_origen = session["sucursal_id"]
    id_sucursal_destino = request.form["id_sucursal_destino"]
    detalle_json = json.loads(request.form["detalle_json"])

    fecha = datetime.now().strftime("%Y-%m-%d")

    db.agregar_pedido(
        id_sucursal_origen,
        id_sucursal_destino,
        fecha,
        "pendiente"
    )

    id_pedido = db.cursor.lastrowid

    for item in detalle_json:
        db.agregar_detalle_pedido(
            id_pedido,
            item["id_producto"],
            item["cantidad_solicitada"],
            0
        )

    return redirect(url_for("gestion_pedidos"))

@app.route("/actualizar_estado_pedido/<int:id_pedido>/<accion>")
def actualizar_estado_pedido(id_pedido, accion):
    db_local = Connexion("database.db")

    if accion == "aprobar":
        nuevo_estado = "aprobado"
    elif accion == "rechazar":
        nuevo_estado = "rechazado"
    else:
        nuevo_estado = "pendiente"

    db_local.cursor.execute("""
        UPDATE pedido 
        SET estado = ?
        WHERE id = ?
    """, (nuevo_estado, id_pedido))

    db_local.conexion.commit()
    db_local.conexion.close()

    return redirect(url_for("gestion_pedidos"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))