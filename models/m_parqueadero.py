from conexion import *

class Parqueadero:

    def consultarEspacios(self, nit):
        sql = """
            SELECT capacidad_carros,
                   capacidad_motos,
                   operaciones_carro,
                   operaciones_moto
            FROM parqueadero
            WHERE nit = %s
        """
        mi_cursor.execute(sql, (nit,))
        return mi_cursor.fetchone()  # 👈 CLAVE
    

    def modificarEspacios(self, nit, capacidad_carro, capacidad_motos):
        sql = """
            UPDATE parqueadero
            SET capacidad_carros = %s,
                capacidad_motos = %s
            WHERE nit = %s
        """
        mi_cursor.execute(sql, (capacidad_carro, capacidad_motos, nit))
        mi_db.commit()

mi_parqueadero = Parqueadero()
