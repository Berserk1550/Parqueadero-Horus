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
    if session.get("login") == True:
        if request.method == "GET":
            # Si es GET, solo muestra el formulario para agregar o modificar espacios
            return render_template("agregar_espacios.html")
        
        if request.method == "POST":
            # Si es POST, significa que se enviaron los datos del formulario
            
            # Obtiene el NIT del parqueadero desde la sesión
            nit = session.get("parqueadero_nit")
            
            # Obtiene las capacidades enviadas por el formulario y las convierte a enteros
            capacidad_carro = int(request.form["capacidad_carros"])
            capacidad_motos = int(request.form["capacidad_motos"])

            # Llama a la función que actualiza las capacidades en la base de datos
            datos = mi_parqueadero.modificarEspacios(
                nit,
                capacidad_carro,
                capacidad_motos
            )

        # Redirige de nuevo a la página principal del parqueadero después de modificar
        return redirect("/parqueadero")
    else:
        return redirect("/")
