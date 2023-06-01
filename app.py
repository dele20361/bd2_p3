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
        if request.form['submit'] == 'Crear Pelicula':
            # Lógica para crear una película en la base de datos
            # Extraer los datos del formulario
            adult = request.form['adult']
            genres = request.form['genres']
            ids = request.form['ids']
            language = request.form['lenguage']
            company = request.form['nombres']
            datetime = request.form['datetime']
            title = request.form['title']
            vote_average = request.form['vote_average']
            # Ejecutar el query de creación de película en la base de datos
            appNeo.createmovie(adult, genres, ids, language, company, datetime, title, vote_average)
            
        elif request.form['submit'] == 'Crear Staff':
            # Lógica para crear un miembro del staff en la base de datos
            # Extraer los datos del formulario
            nombres = request.form['nombres']
            gender = request.form['gender']
            ids = request.form['ids']
            nationality = request.form['nationality']
            rol = request.form['rol']
            correo = request.form['correo']
            # Ejecutar el query de creación de miembro del staff en la base de datos
            appNeo.createstaff(nombres, gender, ids, nationality, rol, correo)
                   
        elif request.form['submit'] == 'Crear Actor':
            # Lógica para crear un actor en la base de datos
            # Extraer los datos del formulario
            nombres = request.form['nombres']
            profile = request.form['profile']
            age = request.form['age']
            gender = request.form['gender']
            ids = request.form['ids']
            # Ejecutar el query de creación de actor en la base de datos
            appNeo.createactor(nombres, profile, age, gender, ids)
            
        elif request.form['submit'] == 'Eliminar':
            # Lógica para realizar la eliminación en la base de datos
            pass
        elif request.form['submit'] == 'Actualizar Pelicula':
            # Lógica para actualizar los datos de la película
            adult = request.form['adult']
            genres = request.form['genres']
            ids = request.form['ids']
            language = request.form['lenguage']
            company = request.form['nombres']
            datetime = request.form['datetime']
            title = request.form['title']
            vote_average = request.form['vote_average']
            
            appNeo.updatemovie(adult, genres, ids, language, company, datetime, title, vote_average)
            
        elif request.form['submit'] == 'Actualizar Staff':
            # Lógica para actualizar los datos del staff
            nombres = request.form['nombres']
            gender = request.form['gender']
            ids = request.form['ids']
            nationality = request.form['nationality']
            rol = request.form['rol']
            correo = request.form['correo']
            
            appNeo.updatestaff(gender, nombres, ids, nationality, rol, correo)
            
        elif request.form['submit'] == 'Actualizar Actor':
            # Lógica para actualizar los datos del actor
            nombres = request.form['nombres']
            profile = request.form['profile']
            age = request.form['age']
            gender = request.form['gender']
            ids = request.form['ids']
            
            appNeo.updateactor(gender, nombres, ids, profile, age)
                
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
