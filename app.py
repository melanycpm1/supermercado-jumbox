from flask import Flask,render_template,session,url_for, redirect,request;
from base_de_datos.mi_conexion import Connexion
import os

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

    db.agregar_usuario("Juan", "Pérez", "admin@correo.com", "1234", "admin", 1)
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
    
    return render_template("panel_principal.html")

@app.route("/gestion_inventario")
def gestion_inventario():
    if "rol" not in session:
        return redirect(url_for("login"))  # si no está logueado
    
    if session["rol"] == "vendedor":
        return "Acceso denegado. No tenés permisos para entrar acá.", 403 #solo ingresaran los usuarios administradores,encargado
    
    return #agregar tamblate

@app.route("/gestion_pedidos")
def gestion_pedidos():
    if "rol" not in session:
        return redirect(url_for("login"))  # si no está logueado
    
    if session["rol"] != "vendedor" or session["rol"] == "reponedor":
        return "Acceso denegado. No tenés permisos para entrar acá.", 403 #solo ingresaran los usuarios administradores, encargado

    return  #agregar tamblate
    
@app.route("/gestion_usuarios")
def gestion_usuario():
    if "rol" not in session:
        return redirect(url_for("login"))  # si no está logueado
    
    if session["rol"] != "admi":
        return "Acceso denegado. No tenés permisos para entrar acá.", 403 #solo ingresaran los usuarios administradores
    
    return #agregar tamblate

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

@app.route("/venta")
def venta():

    if "rol" not in session:
        return redirect(url_for("login"))  # si no está 
    
    if session["rol"] != "vendedor":
        return "Acceso denegado. No tenés permisos para entrar acá.", 403 #solo ingresaran los usuarios administradores
    

    return  #agregar tamblate

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
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))