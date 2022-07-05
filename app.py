from email.mime import message
from flask import Flask, make_response, abort, jsonify, render_template, request, redirect
from models import db,ContactModel
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
	db.create_all()

#Creación de equipo:
@app.route('/create', methods = ['GET'])
def create():
	return render_template('create.html')

@app.route('/create-form', methods = ['GET','POST'])
def createForm():
	pais = request.form['pais']
	idioma = request.form['idioma']
	continente = request.form['continente']
	grupo = request.form['grupo']
	entrenador = request.form['entrenador']
	capitan = request.form['capitan']
	puntaje = request.form['puntaje'] 

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


@app.route('/' , methods = ['GET'])
def RetrieveList():
	contacts = ContactModel.query.all()
	return render_template('index.html', contacts = contacts)



#Actualizando datos:
@app.route('/edit', methods=['GET', 'POST'])
def update():
	if request.method == 'POST':
		id = request.form['id']
		contact = ContactModel.query.filter_by(id=id).first()
		print ("mostrando contacto")
		print (contact)
		db.session.delete(contact) #Elimina el equipo y muestra el modificado 
		db.session.commit()
		if contact:
			contact = ContactModel(
				pais = request.form['pais'],
				idioma = request.form['idioma'],
				continente = request.form['continente'],
				grupo = request.form['grupo'],
				entrenador = request.form['entrenador'],
				capitan = request.form['capitan'],
				puntaje = request.form['puntaje']
			)
			print("Editing...")
			db.session.add(contact)
			db.session.commit()
			return redirect('/')
		return f"El equipo con id = {id} No existe"

	return render_template('update.html', contact = contact)

#Mostramos los datos del update(edit):
@app.route('/<int:id>/edit', methods = ['GET'])
# @app.route('/edit/<int:id>', methods = ['GET'])
def returnUpdate(id):
	contact = ContactModel.query.filter_by(id=id).first()
	return render_template('update.html', contact = contact)



#Eliminamos un equipo:
@app.route('/<int:id>/delete', methods=['GET', 'POST'])

def delete(id):
	contacts = ContactModel.query.filter_by(id=id).first()
	if request.method == 'POST':
		if contacts:
			db.session.delete(contacts)
			db.session.commit()
			return redirect('/')
		abort(404)
		#return redirect('/')
	return render_template('delete.html')

# Empleamos debug=true para que se actualice 
# automáticamente los cambios en el local:
app.run(host='0.0.0.0', port=5001, debug=True)