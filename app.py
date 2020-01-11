from flask import Flask
from flask import render_template, request, session
from flask import redirect, url_for
from flask import flash
from config import Configuracion_desarrollo
from models import User, db, Representante, Preinscripcion
from tables import Tabla
import forms
app = Flask(__name__)
app.config.from_object(Configuracion_desarrollo)


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ["RegistroAlumno"]:
        return redirect(url_for('login'))
    if 'username' in session and request.endpoint in ['registro', 'login']:
        return redirect(url_for("inicio"))


@app.route('/')
def inicio():

    if 'username' in session:
        print(session)
        return "estas logeado"
    return "inicio"


@app.route('/loggin', methods=['GET', 'POST'])
def login():
    hola = forms.loggin(request.form)
    if request.method == 'POST'and hola.validate():
        username = hola.username.data
        password = hola.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.comparar(password):
            susseces_message = "bienbenido{}".format(username)
            flash(susseces_message)
            session['username'] = username
            session['user_id'] = user.id
            return redirect(url_for("inicio"))
        else:
            error_message = "usuario o contraseña invalida"
            flash(error_message)
        session['username'] = hola.username.data

    return render_template("loggin.html", forms=hola)


@app.route('/salir')
def salir():
    """
    esta ruta es para eliminar la cookie session

    """
    if 'username' in session:
        session.pop('username')
    return redirect(url_for("login"))


@app.route("/index")
def index():
    pass


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    """
    esta ruta da el formulario de registro.

    """
    # objeto formulario para pasarlo a jinja2
    hola = forms.Formulario(request.form)
    # si la respuesta del formulario es de tipo post y si no tiene errores
    # entonces crea una instancia Users y rellena para agregarlo a la base
    # la tabla Users
    if request.method == 'POST' and hola.validate():
        user = User(hola.nombre.data, hola.cedula.data,
                    hola.username.data, hola.email.data,
                    hola.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('crea_usuarios.html', forms=hola)


@app.route("/RegistroAlumno",methods=['GET','POST'])
def RegistroAlumno():
    registro = forms.RegistroAlumno(request.form)
    id_representante = Representante.query.get(session['user_id'])
    if request.method == 'POST' and registro.validate():
        preInscrito = Preinscripcion(nombre= registro.nombre.data,
                                    apellido=registro.apellido.data,
                                    escuela= registro.escuela.data,
                                    edad = registro.edad.data, 
                                    Representantes = id_representante)
        db.session.add(preInscrito)
        db.session.commit()
    return render_template("registroAlumnos.html", forms = registro)


@app.route("/Representantes")
def Representantes():
    """
    esta ruta es para guardar los datos la repesentantes de manera automatica
    si todo esta bien no tienen que percatarse de lo que esta pasando :V
    """
    # objeto consulta que filtra si el usuario esta en la tabla Representantes
    representante = Representante.query.filter_by(
        id_usuario=session['user_id']).first()

    # objeto consulta que obtiene el id del usuario segun el id que tiene
    # en la session
    user = User.query.get(session['user_id'])

    if representante is None:
        print(representante)
        print(user)
        r = Representante(Users=user)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('inicio'))

    elif representante.id_usuario == user.id:
        return redirect(url_for('inicio'))

    print(representante)
    print(user)
    return redirect(url_for('inicio'))


@app.route("/eliminar/<int:id>")
def eliminar(id):
    pass
@app.route('/tabla')
def tabla():
    """
    para hacer los join se tiene que utilizar el objeto instancia de sqlalchemy
    porque para el join tienes que hacerlo directamente desde la sesion, agregando las tablas
    que quieres consultar en el espacio de query seguido de la instruccion join y como parametro
    la clase con la que queremos cruzar la consulta, el ultimo paso es para agregar tablas 
    especificas para facilitar la generacion de tablas.

    """
    repre = db.session.query(User,Representante).join(User).add_columns(User.username,User.email
        , Representante.id)
    
    tablita = Tabla(repre)
    return render_template("tabla.html",tabla=tablita)


@app.route('/edita/<id>', methods=["GET", "POST"])
def edita(id):
    id = id

    return "tu id es: {}".format(id)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=7000)
