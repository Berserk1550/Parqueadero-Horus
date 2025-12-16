from conexion import *  # Importa la conexión y el cursor de la base de datos
from routes.r_usuarios import login  # Importa el módulo de login (no usado directamente aquí)
from models.m_parqueadero import *  # Importa la clase Parqueadero y su instancia

# -----------------------------------------
# RUTA PRINCIPAL DEL PARQUEADERO
# -----------------------------------------

# -----------------------------------------
# RUTA PARA CONSULTAR ESPACIOS
# -----------------------------------------
@programa.route("/consultar_espacios")
def consultarEspacio():
    nit = session["parqueadero_nit"]

    # Llama al método del modelo corregido
    respuesta = mi_parqueadero.consultarEspacios(nit)

    # Envía los datos al template
    return render_template("consultar_espacios.html", espacios=respuesta)

# -----------------------------------------
# RUTA PARA MODIFICAR/AGREGAR ESPACIOS
# -----------------------------------------
@programa.route("/espacios/modificar", methods=["GET", "POST"])
def modificar_espacios():

    if not session.get("login"):
        return redirect("/")

    nit = session.get("parqueadero_nit")

    if request.method == "GET":
        espacios = mi_parqueadero.consultarEspacios(nit)

        return render_template(
            "agregar_espacios.html",
            espacios=espacios
        )

    if request.method == "POST":
        capacidad_carro = int(request.form["capacidad_carros"])
        capacidad_motos = int(request.form["capacidad_motos"])

        mi_parqueadero.modificarEspacios(
            nit,
            capacidad_carro,
            capacidad_motos
        )

        return redirect("/opciones")


