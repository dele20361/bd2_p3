from flask import Flask, render_template, request
from system import App

app = Flask(__name__, template_folder='template', static_folder='static')

# @app.route('/')
# def platfomr():
#     # Obtener titulo e imagen de plataforma
#     result = appNeo.find_platform()
#     platformsInfo = {}
#     for record in result:
#         platform_name = record["name"]
#         image_link = record["image_link"]
#         platformsInfo[platform_name] = image_link

#     platformsNames = list(platformsInfo.keys())[-10:]
#     platformsImg = [platformsInfo[key] for key in platformsNames]
    
#     return render_template('platform.html', platformsNames=platformsNames, platformsImg=platformsImg)

@app.route('/', methods=['GET', 'POST'])
def loginr():
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


if __name__ == '__main__':
    uri = "neo4j+s://85d17210.databases.neo4j.io"
    user = "neo4j"
    password = "8_aBrbwezxsQxvPsIhl2UobQu-UQCH65zP6Da58Nplo"
    appNeo = App(uri, user, password)
    app.run()
    appNeo.close()
