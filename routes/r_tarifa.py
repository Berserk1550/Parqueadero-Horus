from conexion import *
from routes.r_usuarios import login
from models.m_tarifa import *

@programa.route("/tarifas")
def tarifas():
    return render_template("tarifas.html")

@programa.route("/consultar_tarifas")
def consultarTarifas():
    
    nit = session["parqueadero_nit"]
    
    respuesta = mi_tarifa.consultarTarifas(nit)
    
    print(respuesta)
    
    return render_template("consultar_tarifas.html", tarifas = respuesta)

@programa.route("/crear_tarifas", methods=["GET", "POST"])
def crearTarifa():
    if request.method == "POST":
        
        nit = session["parqueadero_nit"]
        
        tarifa = request.form["tipo_tarifa"]
        horario_tarifa = request.form["horario"]
        vehiculo = request.form["tipo_vehiculo"]
        valor = request.form["valor_tarifa"]
        hora_comienzo = request.form["hora_inicio"]
        hora_final = request.form["hora_fin"]
        
        repuesta = mi_tarifa.crearTarifas(nit, tarifa, horario_tarifa, vehiculo, valor, hora_comienzo, hora_final)
        
    return render_template("crear_tarifas.html")

@programa.route("/modificar_tarifa/<int:id_tarifa>", methods=["GET"])
def modificar_tarifa(id_tarifa):
    tarifa = mi_tarifa.consultarTarifaPorID(id_tarifa)
    print(tarifa['hora_fin'])
    return render_template("modificar_tarifa.html", tarifa=tarifa)

@programa.route("/modificar_tarifa/<int:id_tarifa>", methods=["POST"])
def actualizar_tarifa(id_tarifa):

    nit_parqueadero = session["parqueadero_nit"]
    tipo_tarifa = request.form["tipo_tarifa"]
    horario = request.form["horario"]
    tipo_vehiculo = request.form["tipo_vehiculo"]
    valor_tarifa = request.form["valor_tarifa"]
    hora_inicio = request.form["hora_inicio"]
    hora_fin = request.form["hora_fin"]

    mi_tarifa.actualizarTarifa(id_tarifa,nit_parqueadero, tipo_tarifa,horario, tipo_vehiculo, valor_tarifa, hora_inicio, hora_fin)

    return redirect("/consultar_tarifas")

@programa.route("/eliminar_tarifa/<int:id_tarifa>", methods=["POST"])
def eliminar_tarifa(id_tarifa):
    resultado = mi_tarifa.eliminarTarifa(id_tarifa)
    
    if resultado == "ok":
        return redirect("/consultar_tarifas")  # Redirige a la lista de tarifas
    else:
        return "Error al eliminar la tarifa", 500