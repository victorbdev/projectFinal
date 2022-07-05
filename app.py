from email.mime import message
from flask import Flask, make_response, abort, jsonify, render_template, request, redirect
from sqlalchemy import true
from models import db,ContactModel
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
	db.create_all()

#creación:
@app.route('/create', methods = ['GET'])
def create():
	return render_template('create.html')

@app.route('/create-form', methods = ['GET','POST'])
def createForm():
	#capitan = request.form.getlist('capitan')
	#capitan = ','.join(map(str, capitan))
	pais = request.form['pais']
	idioma = request.form['idioma']
	continente = request.form['continente']
	grupo = request.form['grupo']
	entrenador = request.form['entrenador']
	capitan = request.form['capitan']
	puntaje = request.form['puntaje'] #quitar el request


	#print ("Contactos modelo")
#Pasatiempo = capitan
	contacts = ContactModel(
		pais = pais,
		idioma = idioma,
		continente = continente,
		grupo = grupo,
		entrenador = entrenador,
		capitan = capitan,
		puntaje = puntaje
	)
	db.session.add(contacts)
	db.session.commit()
	return redirect('/')
	#print ("return something")
	#return make_response(jsonify({"message": "bien"}), 200)


@app.route('/' , methods = ['GET'])
def RetrieveList():
	contacts = ContactModel.query.all()
	return render_template('index.html', contacts = contacts)



#Actualizando datos:
# @app.route('/edit-form', methods=['GET', 'POST'])
@app.route('/edit', methods=['GET', 'POST'])
def update():
	id = request.form['id']
	contact = ContactModel.query.filter_by(id=id).first()
	print ("mostrando contacto")
	print (contact)

	if request.method == 'POST':
		#db.session.delete(contact)
		db.session.commit()
		if contact:
			# capitan = request.form.getlist('capitan')
			# #pasatiempos = ','.join(map(str, pasatiempo))
			# capitan = ",".join(map(str, capitan))
			# pais = request.form['pais']
			# idioma = request.form['idioma']
			# continente = request.form['continente']
			# grupo = request.form['grupo']
			# entrenador = request.form['entrenador']
			# capitan = capitan
			# puntaje = request.form['puntaje']

			#capitan = request.form.getlist('capitan')
			#pasatiempos = ','.join(map(str, pasatiempo))
			#capitan = ",".join(map(str, capitan))
			pais = request.form['pais']
			idioma = request.form['idioma']
			continente = request.form['continente']
			grupo = request.form['grupo']
			entrenador = request.form['entrenador']
			capitan = request.form['capitan']
			puntaje = request.form['puntaje']


			print ("Contactos modelo")
			contact = ContactModel(
				pais = pais,
				idioma = idioma,
				continente = continente,
				grupo = grupo,
				entrenador = entrenador,
				capitan = capitan,
				puntaje = puntaje
			)
			db.session.add(contact)
			db.session.commit()
			#return redirect('/')
			return f"El equipo con id = {id}COMIDA"
			#print ("return something")
		return f"El equipo con id = {id} No existe"
		

	return render_template('update.html', contact = contact)



#Mostrando datos del update:
@app.route('/<int:id>/edit', methods = ['GET'])
# @app.route('/edit/<int:id>', methods = ['GET'])
def returnUpdate(id):
	contact = ContactModel.query.filter_by(id=id).first()
	return render_template('update.html', contact = contact)



#Eliminar el contact:
@app.route('/<int:id>/delete', methods=['GET', 'POST'])

def delete(id):
	contacts = ContactModel.query.filter_by(id=id).first()
	if request.method == 'POST':
		if contacts:
			db.session.delete(contacts)
			db.session.commit()
			return redirect('/')
		abort(404)
		#return redirect('/')#depende habilitar
	return render_template('delete.html')

app.run(host='localhost', port=5000)