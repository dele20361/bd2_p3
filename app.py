from flask import Flask, render_template, request
from system import App

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
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
    


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/editMovie')
def editMovie():
    return render_template('editarMovie.html')

@app.route('/editUser')
def editUser():
    return render_template('editarUser.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/editPlatform')
def editPlatform():
    return render_template('editPlatform.html')

if __name__ == '__main__':
    uri = "neo4j+s://85d17210.databases.neo4j.io"
    user = "neo4j"
    password = "8_aBrbwezxsQxvPsIhl2UobQu-UQCH65zP6Da58Nplo"
    appNeo = App(uri, user, password)
    app.run()
    appNeo.close()
