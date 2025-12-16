import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import *

class Usuario:
    
    def loguear(self, cedula):
        sql = """SELECT cedula, nombres, apellidos, rol, activo, parqueadero_nit FROM usuarios WHERE cedula = %s AND activo = %s"""
        estado = "activo"
        mi_cursor.execute(sql, (cedula, estado,))
        resultado = mi_cursor.fetchall()
        return resultado
    
    
    def consultarUsuario(self,nit):
        
        sql = "SELECT cedula, nombres, apellidos, correo, telefono, tel_emergencia, fecha_registro FROM usuarios WHERE parqueadero_nit = %s AND rol = %s AND activo = %s"
        rol = "portero"
        estado = "activo"
        mi_cursor.execute(sql,(nit,rol,estado,))
        resultado = mi_cursor.fetchall()
        
        return resultado

    def ingresar_usuario(self, cedula, nombres, apellidos, correo, telefono, tel_emergencia, rol, parqueadero_nit, fecha_registro):
        sql="INSERT INTO usuarios (cedula, nombres, apellidos, correo, telefono, tel_emergencia, rol, parqueadero_nit, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mi_cursor.execute(sql,(cedula, nombres, apellidos, correo, telefono, tel_emergencia, rol, parqueadero_nit, fecha_registro))
        mi_db.commit()
        
    
    def consultarUsuarioPorCedula(self, cedula):
        sql = """
                SELECT cedula, nombres, apellidos, correo, telefono, tel_emergencia
                FROM usuarios
                WHERE cedula = %s
            """
        mi_cursor.execute(sql, (cedula,))
        resultado = mi_cursor.fetchone()
        print("si entro a consultar por cedula")
        return resultado

    def actualizarUsuario(self, cedula, nombres, apellidos, correo, telefono, tel_emergencia):
        sql = """
            UPDATE usuarios
            SET nombres=%s, apellidos=%s, correo=%s, telefono=%s, tel_emergencia=%s
            WHERE cedula=%s
        """
        valores = (nombres, apellidos, correo, telefono, tel_emergencia, cedula)
        mi_cursor.execute(sql, valores)
        mi_db.commit()
        print("si entro a actualizar usuario")
        return "ok"

    def eliminarUsuario(self, cedula):
        sql = """
            UPDATE usuarios
            SET activo = 'inactivo'
            WHERE cedula = %s
        """
        mi_cursor.execute(sql, (cedula,))
        mi_db.commit()
        return "ok"

mi_usuario = Usuario()

#if __name__ == "__main__":
#    print("Importación exitosa. Conexión establecida.")
#EMILY DEBES HACER UN CONDIC<IONAL PARA EL CALCULO FINAL DE LAS TARIFAS, SEGUN LE CONVENGA AL CLIENTE POR EL TIEMPOP QUE EN SU DEFECTO PASE EL VEHICULO EN EL PARQUEADERO
