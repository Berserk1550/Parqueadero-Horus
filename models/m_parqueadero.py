from conexion import *

class Parqueadero:

    def consultarEspacios(self, nit):
        sql = "SELECT capacidad_carros,capacidad_motos,operaciones_carro,operaciones_moto FROM parqueadero WHERE nit = %s"
        mi_cursor.execute(sql, (nit,))  
        resultado = mi_cursor.fetchall()
        return resultado

    
    def modificarEspacios(self,nit,capacidad_carro,capacidad_motos):
        # Define el SQL para actualizar las capacidades del parqueadero
        sql = "UPDATE parqueadero SET capacidad_carros =%s, capacidad_motos =%s WHERE nit = %s"
        
        # Ejecuta el UPDATE en la base de datos con los valores recibidos
        mi_cursor.execute(sql, (capacidad_carro, capacidad_motos, nit))
        # Confirma los cambios en la base de datos
        mi_db.commit()

mi_parqueadero = Parqueadero()