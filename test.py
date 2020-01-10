from models import User, Representante ,Preinscripcion, db


u = User("cesar", "24370551", "cesardaval", "cesarhquinterod@gmail.com"
	, "proquinteroXDXD")

r = Representante(Users=u)

p = Preinscripcion(nombre="juan",apellido="quintero"
	,edad="12",escuela="Rafael Urdaneta",Representantes=r)

db.session.add(u)
db.session.add(r)
db.session.add(p)
db.session.commit()