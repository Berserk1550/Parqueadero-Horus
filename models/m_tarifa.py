from conexion import *


class Tarifas:

    # Función que consulta todas las tarifas de un parqueadero
    def consultarTarifas(self, nit):
        sql = """
            SELECT id_tarifas, tipo_tarifa, horario, tipo_vehiculo,
                valor_tarifa, hora_inicio, hora_fin
            FROM tarifas
            WHERE parqueadero_nit = %s
            AND activo = "activo"
        """
        # Ejecuta la consulta con el parámetro del NIT
        mi_cursor.execute(sql, (nit,))
        resultado = mi_cursor.fetchall()

        # Recorre los resultados y convierte hora_inicio y hora_fin
        # de timedelta a formato de 12 horas con minutos y AM/PM
        for r in resultado:
            if isinstance(r["hora_inicio"], timedelta):
                segundos = r["hora_inicio"].seconds
                r["hora_inicio"] = (datetime.min + r["hora_inicio"]).strftime("%I:%M %p").lstrip("0")
            if isinstance(r["hora_fin"], timedelta):
                segundos = r["hora_fin"].seconds
                r["hora_fin"] = (datetime.min + r["hora_fin"]).strftime("%I:%M %p").lstrip("0")
        
        return resultado

    # Función que consulta una tarifa específica por ID
    def consultarTarifaPorID(self, id_tarifa):
        sql = """
            SELECT id_tarifas, tipo_tarifa, horario, tipo_vehiculo, valor_tarifa,
                hora_inicio, hora_fin
            FROM tarifas
            WHERE id_tarifas = %s
        """
        mi_cursor.execute(sql, (id_tarifa,))
        resultado = mi_cursor.fetchone()

        if resultado:
            # Convierte los valores de timedelta a formato HH:MM 24 horas
            if isinstance(resultado['hora_inicio'], timedelta):
                segundos = resultado['hora_inicio'].seconds
                resultado['hora_inicio'] = f"{segundos // 3600:02d}:{(segundos % 3600)//60:02d}"
            if isinstance(resultado['hora_fin'], timedelta):
                segundos = resultado['hora_fin'].seconds
                resultado['hora_fin'] = f"{segundos // 3600:02d}:{(segundos % 3600)//60:02d}"
        
        return resultado

    # Función para crear una nueva tarifa
    def crearTarifas(self, nit, tipo_tarifa, horario, tipo_vehiculo, valor_tarifa, hora_inicio, hora_fin):
        sql = """
            INSERT INTO tarifas (parqueadero_nit, tipo_tarifa, horario, tipo_vehiculo,
                                valor_tarifa, hora_inicio, hora_fin)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nit, tipo_tarifa, horario, tipo_vehiculo, valor_tarifa, hora_inicio, hora_fin)
        mi_cursor.execute(sql, valores)
        mi_db.commit()  # Guarda los cambios en la base de datos

    # Función para verificar si ya existe una tarifa duplicada
    def existeTarifaDuplicada(self, nit, tipo_tarifa, horario, tipo_vehiculo, hora_inicio, hora_fin, id_actual):
        sql = """
            SELECT id_tarifas
            FROM tarifas
            WHERE parqueadero_nit = %s
                AND tipo_tarifa = %s
                AND horario = %s
                AND tipo_vehiculo = %s
                AND hora_inicio = %s
                AND hora_fin = %s
                AND id_tarifas <> %s
        """
        valores = (nit, tipo_tarifa, horario, tipo_vehiculo, hora_inicio, hora_fin, id_actual)
        mi_cursor.execute(sql, valores)
        resultado = mi_cursor.fetchone()
        # Devuelve True si existe duplicado, False si no existe
        return resultado is not None

    # Función para actualizar una tarifa existente
    def actualizarTarifa(self, id_tarifa, nit, tipo_tarifa, horario, tipo_vehiculo, valor_tarifa, hora_inicio, hora_fin):
        # Verifica si existe una tarifa duplicada antes de actualizar
        if self.existeTarifaDuplicada(nit, tipo_tarifa, horario, tipo_vehiculo, hora_inicio, hora_fin, id_tarifa):
            return "duplicado"

        sql = """
            UPDATE tarifas
            SET tipo_tarifa = %s,
                horario = %s,
                tipo_vehiculo = %s,
                valor_tarifa = %s,
                hora_inicio = %s,
                hora_fin = %s
            WHERE id_tarifas = %s
        """
        valores = (tipo_tarifa, horario, tipo_vehiculo, valor_tarifa, hora_inicio, hora_fin, id_tarifa)
        mi_cursor.execute(sql, valores)
        mi_db.commit()
        return "ok"

    def eliminarTarifa(self, id_tarifa):
        sql = """
            UPDATE tarifas
            SET activo = 'inactivo'
            WHERE activo = 'activo'
                AND id_tarifas = %s
        """
        valores = (id_tarifa,)  # Tupla de un solo elemento
        mi_cursor.execute(sql, valores)
        mi_db.commit()  # Confirmar cambios en la base de datos
        return "ok"

# Instancia de la clase Tarifas para usarla en rutas
mi_tarifa = Tarifas()
