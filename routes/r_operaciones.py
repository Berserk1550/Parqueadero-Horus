from conexion import *
from flask import jsonify
from models.m_operaciones import mi_operacion
from models.m_tarifa import mi_tarifa

@programa.route("/operaciones", methods=['GET'])
def operaciones():
    if not session.get("login"):
        return redirect('/')
    parqueadero_nit = session.get("parqueadero_nit")
    activos = mi_operacion.vehiculos_activos(parqueadero_nit)
    registros = mi_operacion.registros_previos(parqueadero_nit)

    conteo_carros = len([v for v in activos if str(v.get('tipo_vehiculo', '')).upper == 'CARRO'])
    conteo_motos = len([v for v in activos if str(v.get('tipo_vehiculo', '')).upper == 'MOTO'])
    return render_template("operaciones.html", activos=activos, registros=registros, conteo_carros=conteo_carros, conteo_motos=conteo_motos)

@programa.route("/operaciones/ingreso", methods=['POST'])
def ingreso():
    if not session.get("login"):
        return jsonify({"ok": False, "error": "no_session"}), 401
    
    vehiculo_placa = request.form.get('vehiculo_placa', '').strip().upper()
    tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip().upper()
    usuario_cedula = session.get('usuario_cedula')
    parqueadero_nit = session.get('parqueadero_nit')
    
    if len(vehiculo_placa) !=6:
        return jsonify({"ok": False, "error": "placa_invalida", "mensaje": "La placa debe tener 6 caracteres"}), 400
    if tipo_vehiculo == "CARRO":
        if not all(c.isalpha() for c in vehiculo_placa[:3]):
            return jsonify({"ok": False, "error": "placa_invalida", "mensaje": "Para Carro Los primeros 3 caracteres deben ser letras"}), 400
        if not all(c.isdigit() for c in vehiculo_placa[3:]):
            return jsonify({ "ok": False, "error": "placa_invalida", "mensaje": "Los últimos 3 caracteres deben ser números (0-9). "}), 400
    elif tipo_vehiculo == "MOTO":
        if not all(c.isalpha() for c in vehiculo_placa[:3]):
            return jsonify({"ok": False, "error": "placa_invalida", "mensaje": "Para Moto Los primeros 3 caracteres deben ser letras"}), 400  
        if not all(c.isdigit() for c in vehiculo_placa[3:5]):
            return jsonify({"ok": False, "error": "placa_invalida", "mensaje": "Ls caracteres 4 y 5 para moto deben ser números."}), 400
        if not vehiculo_placa[5].isalpha():
            return jsonify({"ok": False, "error": "placa_invalida", "mensaje": "El ultimo caracter en la placa de moto debe ser Letra (A-Z)"}), 400
    else:
        return jsonify({"ok": False, "error": "tipo_invalido", "mensaje": "Tipo de vehicu.o no reconocido"}), 400
    
    sql_check = """SELECT COUNT(*) AS total FROM registros WHERE vehiculo_placa=%s AND parqueadero_nit=%s AND fecha_salida IS NULL"""
    mi_cursor.execute(sql_check, (vehiculo_placa, parqueadero_nit))
    resultado = mi_cursor.fetchone()
    if resultado['total'] > 0:
        return jsonify({"ok": False, "error": "ya_activo"}),409
    
    tarifas = mi_tarifa.consultarTarifas(parqueadero_nit)
    tarifa_usada = next((t for t in tarifas if str(t['tipo_vehiculo']).upper() == tipo_vehiculo), None)
    if not tarifa_usada:
        return jsonify({"ok": False, "error": "sin_tarifa"}), 404
    
    sql_insert = """INSERT INTO registros (vehiculo_placa, usuario_cedula, parqueadero_nit, fecha_ingreso, activo, tarifa_id) VALUES (%s,%s,%s, NOW(), 'activo', %s)"""
    mi_cursor.execute(sql_insert, (vehiculo_placa, usuario_cedula, parqueadero_nit, tarifa_usada['id_tarifas']))
    mi_db.commit()
    return jsonify({"ok": True, "vehiculo_placa": vehiculo_placa, "tipo_vehiculo": tipo_vehiculo})

@programa.route("/operaciones/salida", methods=['POST'])
def salida():
    if not session.get("login"):
        return jsonify({"ok": False, "error": "no_session"}), 401
    
    vehiculo_placa = request.form.get('vehiculo_placa', '').strip().upper()
    parqueadero_nit = session.get('parqueadero_nit')
    
    sql_activo = """SELECT r.id_registros, r.fecha_ingreso, r.tarifa_id, t.tipo_vehiculo FROM registros r JOIN tarifas t ON r.tarifa_id = t.id_tarifas WHERE r.vehiculo_placa=%s AND r.parqueadero_nit=%s AND r.fecha_salida IS NULL LIMIT 1"""
    mi_cursor.execute(sql_activo,(vehiculo_placa, parqueadero_nit))
    reg = mi_cursor.fetchone()
    if not reg:
        return jsonify({"ok": False, "error": "no_activo"}), 404
    
    id_registros, fecha_ingreso, tipo_vehiculo, tarifa_id = reg['id_registros'], reg['fecha_ingreso'], reg['tipo_vehiculo'], reg['tarifa_id']
    
    sql_min = "SELECT TIMESTAMPDIFF(MINUTE, %s, NOW()) AS minutos"
    mi_cursor.execute(sql_min, (fecha_ingreso,))
    minutos = mi_cursor.fetchone()['minutos']
    
    tarifas = mi_tarifa.consultarTarifas(parqueadero_nit)
    tarifa_usada = next((t for t in tarifas if t['id_tarifas'] == tarifa_id), None)
    if not tarifa_usada:
        return jsonify({"ok": False, "error": "sin_tarifa"}), 404
    
    valor_base = tarifa_usada['valor_tarifa']
    if minutos <=60 and tarifa_usada['tipo_tarifa'] == 'primera_hora':
        total = valor_base
    elif tarifa_usada['tipo_tarifa'] == 'hora_extra':
        horas = (minutos - 60 + 59) // 60 if minutos > 60 else 0
        total = valor_base + max(horas, 1)
    else:
        total = valor_base
        
    sql_update = """UPDATE registros SET fecha_salida = NOW(), total = %s, activo='inactivo', tarifa_id=%s WHERE id_registros=%s"""
    mi_cursor.execute(sql_update,(total, tarifa_id, id_registros))
    mi_db.commit()
    
    return jsonify({"ok": True, "vehiculo_placa": vehiculo_placa, "tipo_vehiculo": tipo_vehiculo, "fecha_ingreso": str(fecha_ingreso), "fecha_salida": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "minutos": minutos, "tarifa": tarifa_usada, "total": float(total)})

@programa.route("/operaciones/vehiculos_activos", methods=['GET'])
def vehiculos_activos():
    if not session.get("login"):
        return redirect('/')
    parqueadero_nit = session.get("parqueadero_nit")
    operaciones = mi_operacion.vehiculos_activos(parqueadero_nit)
    return render_template("operaciones_activos.html", operaciones=operaciones)

@programa.route("/operaciones/registros_previos", methods=['GET'])
def registros_previos():
    if not session.get("login"):
        return redirect('/')
    parqueadero_nit = session.get("parqueadero_nit")
    operaciones = mi_operacion.registros_previos(parqueadero_nit)
    return render_template("operaciones_historico.html", operaciones=operaciones)