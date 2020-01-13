"""from models import User, Representante ,Preinscripcion, db


u = User("cesar", "24370551", "cesardaval", "cesarhquinterod@gmail.com"
	, "proquinteroXDXD")

r = Representante(Users=u)

p = Preinscripcion(nombre="juan",apellido="quintero"
	,edad="12",escuela="Rafael Urdaneta",Representantes=r)

db.session.add(u)
db.session.add(r)
db.session.add(p)
db.session.commit()

"""
from flask import Flask, render_template,url_for
from flask_weasyprint import HTML, render_pdf
from models import User, db, Representante, Preinscripcion
from tables import Tabla
from config import Configuracion_desarrollo
app = Flask(__name__)
app.config.from_object(Configuracion_desarrollo)


@app.route('/reporte.pdf')
def hola():
	repre = db.session.query(User,Representante).join(User).add_columns(User.username,User.email
        , Representante.id)
	tablita = Tabla(repre)
	prueba = render_template("tabla.html", tabla=tablita)


	return render_pdf(HTML(string=prueba))

@app.route('/edita/<id>', methods=["GET", "POST"])
def edita(id):
    id = id

    return "tu id es: {}".format(id)



@app.route('/hello/', defaults={'name': 'World'})
@app.route('/hello/<name>/')
def hello_html(name):
    return render_template('hello.html', name=name)


# Alternatively, if the PDF does not have a matching HTML page:

@app.route('/hello_<name>.pdf')
def hello_pdf(name):
    # Make a PDF straight from HTML in a string.
    html = render_template('hello.html', name=name)
    return render_pdf(HTML(string=html))




if __name__ == '__main__':
	db.init_app(app)
	app.run(debug=True,port=7000)