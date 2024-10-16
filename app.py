from flask import Flask, request,render_template,redirect,url_for,session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'contactos' in session and len(session['contactos']) > 0:
        return max(item['id'] for item in session['contactos']) + 1
    else:
        return 1

@app.route("/")
def index():
    if 'contactos' not in session:
        session['contactos'] = []
        
    contactos = session.get('contactos',[])
    return render_template('index.html',contactos=contactos)



@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        nombre =  request.form['nombre']
        correo =  request.form['correo']
        celular =  request.form['celular']
        
        nuevo_contacto = {
            'id': generar_id(),
            'nombre':nombre,
            'correo':correo,
            'celular':celular
        }
        
        if 'contactos' not in session:
            session['contactos'] = []
            
        session['contactos'].append(nuevo_contacto)
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_contactos = session.get('contactos',[])
    contacto = next( (c for c in lista_contactos if c['id'] == id), None)
    if not contacto:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        contacto['nombre'] = request.form['nombre']
        contacto['correo'] = request.form['correo']
        contacto['celular'] = request.form['celular']
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html',contacto=contacto)
    
@app.route("/eliminar/<int:id>",methods=["POST"])
def eliminar(id):
    lista_contactos = session.get('contactos',[])
    contacto = next((c for c in lista_contactos if c['id'] == id),None)
    if contacto:
        session['contactos'].remove(contacto)
        session.modified = True
    return redirect(url_for('index'))
        

if __name__ == "__main__":
    app.run(debug=True)