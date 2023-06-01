from flask import Flask, render_template, request
from system import App

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def platfomr():
    # Obtener titulo e imagen de plataforma
    result = appNeo.find_platform()
    platformsInfo = {}
    for record in result:
        platform_name = record["name"]
        image_link = record["image_link"]
        platformsInfo[platform_name] = image_link

    platformsNames = list(platformsInfo.keys())[-10:]
    platformsImg = [platformsInfo[key] for key in platformsNames]
    
    return render_template('platform.html', platformsNames=platformsNames, platformsImg=platformsImg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contra = request.form['contra']
        
        # Validar el inicio de sesión
        # TODO
        result = appNeo.find_Subscribed_by_relationship_property(property_key='email', property_value=correo)
        if len(result) > 0:
            if result[0]['contra'] == contra:
                return render_template('homepage.html')
        else:
            mensaje = "Credenciales inválidas"
        
    else:
        return render_template('logIn.html')
    


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')



@app.route('/editMovie', methods=['GET', 'POST'])
def editMovie():
    if request.method == 'POST':
        if request.form['submit'] == 'Crear':
            # Lógica para realizar la creación en la base de datos
            pass
        elif request.form['submit'] == 'Eliminar':
            # Lógica para realizar la eliminación en la base de datos
            pass
        elif request.form['submit'] == 'Realizar actualizacion':
            if 'title' in request.form:
                # Lógica para actualizar los datos de la película
                adult = request.form['adult']
                genres = request.form['genres']
                ids = request.form['ids']
                Lenguage = request.form['Lenguage']
                nombres = request.form['nombres']
                datetime = request.form['datetime']
                tittle = request.form['tittle']
                vote_average = request.form['vote_average']
                
                appNeo.updatemovie(adult,genres,ids,Lenguage, nombres, datetime,tittle,vote_average)
            elif 'nombres' in request.form and 'rol' in request.form:
                # Lógica para actualizar los datos del staff
                gender = request.form['gender']
                nombres = request.form['nombres']
                ids = request.form['ids']
                nationality = request.form['nationality']
                rol = request.form['rol']
                correo = request.form['correo']
                
                appNeo.updatestaff(gender,nombres,ids,nationality,rol,correo)
                
            elif 'nombres' in request.form and 'age' in request.form:
                # Lógica para actualizar los datos del actor
                gender = request.form['gender']
                nombres = request.form['nombres']
                ids = request.form['ids']
                profile = request.form['profile']
                age = request.form['age']
                
                appNeo.updateactor(gender,nombres,ids,profile,age)
                
    return render_template('editarMovie.html')

@app.route('/editUser', methods=['GET', 'POST'])
def editUser():
    
    if request.method == 'POST':
        if request.form['submit'] == 'Crear':
            # Lógica para realizar la creación en la base de datos
            name = request.form['name']
            country = request.form['country']
            ids = request.form['ids']
            age = request.form['age']
            gender = request.form['gender']
            
            appNeo.createuser(gender,name,ids,country,age)
            
        elif request.form['submit'] == 'Eliminar':
            # Lógica para realizar la eliminación en la base de datos
            pass
        elif request.form['submit'] == 'Realizar actualizacion':
            # Lógica para realizar la actualización en la base de datos
            name = request.form['name']
            country = request.form['country']
            ids = request.form['ids']
            age = request.form['age']
            gender = request.form['gender']
            
            appNeo.updateuser(gender,name,ids,country,age)

    
    return render_template('editarUser.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    return render_template('consulta.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    label = request.form['label']
    old_property = request.form['old_property']
    old_value = request.form['old_value']
    new_property = request.form['new_property']
    new_value = request.form['new_value']
    
    appNeo.update(label, old_property,old_value,new_property,new_value)

    return render_template('update.html')

@app.route('/editPlatform', methods=['GET', 'POST'])
def editPlatform():
    return render_template('editPlatform.html')

if __name__ == '__main__':
    uri = "neo4j+s://85d17210.databases.neo4j.io"
    user = "neo4j"
    password = "8_aBrbwezxsQxvPsIhl2UobQu-UQCH65zP6Da58Nplo"
    appNeo = App(uri, user, password)
    app.run()
    appNeo.close()
