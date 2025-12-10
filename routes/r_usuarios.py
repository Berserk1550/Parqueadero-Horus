from datetime import datetime
from conexion import *
from models.m_usuarios import *

#este metodo se encarga de dar ingreso al programa al usuaurio
@programa.route("/login", methods = ['POST'])
def login():
    
    cedula = request.form["Usuario_C"]
    
    if not re.fullmatch(r"\d{6,10}", cedula):
        
        return render_template("inicio.html", msg="Formato de cédula inválido.")
    
    resultado = mi_usuario.loguear(cedula)
    
    if len(resultado)==0:#<--- si el tamaño de la respuesta es 0 == usuario no existente 
    
        return render_template("inicio.html",msg="Cedula No Registrada.")
    
    else:
        usuario = resultado[0] 
        if usuario["activo"] != "inactivo": #<-- se valida si el usuario esta activo
            session["login"] = True
            session["cedula"] = usuario["cedula"]
            session["nombres"] = usuario["nombres"]
            session["rol"] = usuario["rol"]
            session["activo"] = usuario["activo"]
            session["parqueadero_nit"] = usuario["parqueadero_nit"]
            if usuario["rol"] == "portero":
                return redirect ("/operaciones")
            else:
                return redirect("/opciones")
        else:
            return render_template("index.html",msg="El usuario no esta activo") #<-- si el usuario no esta activo se devuelve un mesensaje informando
        

@programa.route("/cerrar_sesion")
def cerrarSesion():
    session.clear()
    
    return redirect("/")

@programa.route("/admin/consultar_usuario")
def consultarUsuario():
    
    nit = session["parqueadero_nit"]
    
    respuesta = mi_usuario.consultarUsuario(nit)
    
    print(respuesta)
    return render_template("consultar_usuario.html", usuarios = respuesta)

@programa.route('/admin/agregar_usuario', methods=['GET', 'POST'])
def crear_usuario():                            #iniciamos registro del usuario/portero a traves de un admin
    if not session.get("login") or session.get("rol") != "admin":
        return redirect('/')
    
    mensaje=None
    if request.method=='POST':
        cedula=request.form['cedula']
        nombres=request.form['nombres']
        apellidos=request.form['apellidos']
        correo=request.form['correo']
        telefono=request.form['telefono']
        tel_emergencia=request.form['tel_emergencia']
        rol="portero"
        parqueadero_nit = session.get("parqueadero_nit")
        fecha_registro = datetime.today().strftime('%Y-%m-%d')


        mi_usuario.ingresar_usuario(cedula, nombres, apellidos, correo, telefono, tel_emergencia, rol, parqueadero_nit, fecha_registro)
        return redirect("/opciones")
    return render_template("reg_portero.html")  # ← muestra el formulario si no se ha enviado # si no es POST, es GET → mostrar el formulario 

# Mostrar formulario para modificar un usuario
@programa.route("/modificar_usuario/<cedula>", methods=["GET"])
def modificarUsuario(cedula):
    usuario = mi_usuario.consultarUsuarioPorCedula(cedula)
    print("si entro aqui")
    return render_template("modifica_usuario.html", usuario=usuario)

# Guardar cambios del usuario modificado
@programa.route("/admin/modificar_usuario/<cedula>", methods=["POST"])
def actualizarUsuario(cedula):
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]
    tel_emergencia = request.form["tel_emergencia"]

    respuesta = mi_usuario.actualizarUsuario(cedula, nombres, apellidos, correo, telefono, tel_emergencia)
    print(respuesta)
    if respuesta == "ok":
        return redirect("/admin/consultar_usuario")

# Eliminar usuario
@programa.route("/eliminar_usuario/<cedula>", methods=["POST"])
def eliminarUsuario(cedula):
    mi_usuario.eliminarUsuario(cedula)
    return redirect("/admin/consultar_usuario")