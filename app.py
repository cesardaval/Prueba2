from flask import Flask
from flask import render_template, request, session
from flask import redirect, url_for
from flask import flash
from config import Configuracion_desarrollo
from models import User, db, Representante, Preinscripcion

import forms
app = Flask(__name__)
app.config.from_object(Configuracion_desarrollo)


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ["RegistroAlumno"]:
        return redirect(url_for('login'))
    if 'username' in session and request.endpoint in ['registro']:
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
    if 'username' in session:
        session.pop('username')
    return redirect(url_for("login"))


@app.route("/index")
def index():
    pass


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    hola = forms.Formulario(request.form)
    if request.method == 'POST' and hola.validate():
        user = User(hola.nombre.data, hola.cedula.data,
                    hola.username.data, hola.email.data,
                    hola.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('crea_usuarios.html', forms=hola)


@app.route("/RegistroAlumno")
def RegistroAlumno():
    return "estoy en desarrollo"


@app.route("/Representantes")
def Representantes():
    user = User.query.get(session['user_id'])
    r = Representante(Users=user)
    db.session.add(r)
    db.session.commit()
    print(user)
    return "en desarrollo"#redirect(url_for('inicio'))


@app.route("/eliminar/<int:id>")
def eliminar(id):
    pass


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=7000)
