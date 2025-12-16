from conexion import mi_cursor, mi_db
from datetime import datetime
import sys
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Operaciones:
    def ingreso(self, vehiculo_placa, usuario_cedula, parqueadero_nit):
        fecha_ingreso = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO registros (parqueadero_nit, usuario_cedula, vehiculo_placa, fecha_ingreso) VALUES (%s, %s, %s, %s)"""
        mi_cursor.execute(sql,(parqueadero_nit, usuario_cedula, vehiculo_placa, fecha_ingreso))
        mi_db.commit()

    def salida(self, vehiculo_placa):
        fecha_salida = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sql = """UPDATE registros SET fecha_salida =%s WHERE vehiculo_placa = %s AND fecha_salida IS NULL"""
        mi_cursor.execute(sql,(fecha_salida, vehiculo_placa))
        mi_db.commit()

    def vehiculos_activos(self, parqueadero_nit):
        sql = """SELECT r.id_registros, r.vehiculo_placa, r.usuario_cedula, r.fecha_ingreso, t.tipo_vehiculo FROM registros r JOIN tarifas t ON r.tarifa_id = t.id_tarifas WHERE r.parqueadero_nit = %s AND r.fecha_salida IS NULL ORDER BY r.fecha_ingreso DESC"""
        mi_cursor.execute(sql,(parqueadero_nit,))
        return mi_cursor.fetchall()

    def registros_previos(self, parqueadero_nit):
        sql = """SELECT r.id_registros, r.vehiculo_placa, r.parqueadero_nit, r.fecha_ingreso, r.fecha_salida, t.tipo_vehiculo FROM registros r JOIN tarifas t ON r.tarifa_id = t.id_tarifas WHERE r.parqueadero_nit= %s AND r.fecha_salida IS NOT NULL ORDER BY r.fecha_salida DESC"""
        mi_cursor.execute(sql,(parqueadero_nit,))
        return mi_cursor.fetchall()

mi_operacion = Operaciones() 