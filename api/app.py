from flask import Flask, request, jsonify, render_template, session
from flask_restful import Resource, Api
from conexion import conexion, cursor  # Importación directa desde tu nuevo conexion.py
from r_convenios import convenios 
from conexion import *  # Importación directa desde tu nuevo conexion.py

programa = Flask(__name__)
api = Api(programa)

# Ejemplo de recurso: lista de usuarios
class UsuarioLista(Resource):
    def get(self):
        mi_cursor.execute("SELECT * FROM usuarios")
        resultado = mi_cursor.fetchall()
        usuarios = []
        for u in resultado:
            usuarios.append({
                "id": u["id"],
                "nombre": u["nombre"],
                "correo": u["correo"],
                "tipo": u["tipo"],
                "activo": u["activo"]
            })
        return jsonify({"usuarios": usuarios})

# Ejemplo de recurso: usuario individual
class Usuario(Resource):
    def get(self, id):
        mi_cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        u = mi_cursor.fetchone()
        if u:
            return jsonify({
                "id": u["id"],
                "nombre": u["nombre"],
                "correo": u["correo"],
                "tipo": u["tipo"],
                "activo": u["activo"]
            })
        else:
            return jsonify({"mensaje": "Usuario no encontrado"})

# Registro de rutas
api.add_resource(UsuarioLista, "/usuarios")
api.add_resource(Usuario, "/usuarios/<int:id>")

print("tangamandapio")

# Ejecución del servidor
if __name__ == "__main__":
    programa.run(host="0.0.0.0", debug=True, port=8001)
