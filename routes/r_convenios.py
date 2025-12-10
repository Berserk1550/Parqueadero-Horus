from flask import render_template, request, redirect, session
from datetime import datetime
from conexion import *


@programa.route('/convenios', methods=['GET', 'POST'])
def convenios():
    if not session.get("login") or session.get("rol") != "admin":
        return redirect('/')
    if request.method == 'POST':
        tipo_convenio = request.form['tipo_convenio']
        identificacion = request.form['identificacion']
        nombre = request.form['nombre']
        descuento_carro = request.form['descuento_carro']
        descuento_moto = request.form['descuento_moto']
        estado = request.form.get('estado', 'activo')
        parqueadero_nit = session.get("parqueadero_nit")
        fecha_registro = datetime.today().strftime('%Y-%m-%d')

        if not tipo_convenio or not identificacion or not nombre:
            mensaje = "Porfavor Llene Todos Los Campos"
            return render_template("form_convenios.html", msg = mensaje)
        sql = "SELECT * FROM convenios WHERE identificacion = %s"
        mi_cursor.execute(sql, (identificacion,))
        resultado = mi_cursor.fetchall()
        if not descuento_carro or not descuento_moto:
            mensaje = "Los campos de descuento no pueden estar vacíos"
            return render_template("form_convenios.html", msg=mensaje)
        try:
            descuento_carro = int(descuento_carro)
            descuento_moto = int(descuento_moto)
            if descuento_carro < 0 or descuento_moto < 0:
                mensaje = "Los valores del descuento no pueden ser negativos"
                return render_template("form_convenios.html", msg=mensaje)
        except ValueError:
            mensaje = "Los valores de descuento deben ser números enteros"
            return render_template("form_convenios.html", msg=mensaje)

        if resultado:
            mensaje = "El numero de identificacion Ya ha sido registrado a un convenio"
            return render_template("form_convenios.html", msg=mensaje)
        sql_insert = """INSERT INTO convenios (tipo_convenio, identificacion, nombre, descuento_carro, descuento_moto, estado, fecha_registro, parqueadero_nit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        mi_cursor.execute(sql_insert,(tipo_convenio, identificacion, nombre, descuento_carro, descuento_moto, estado, fecha_registro, parqueadero_nit))
        mi_db.commit()
        

        return redirect('/opciones')
    return render_template('form_convenios.html')