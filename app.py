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
        if correo == 'usuario@ejemplo.com' and contra == 'contraseña':
            mensaje = "Inicio de sesión exitoso"
        else:
            mensaje = "Credenciales inválidas"
        
        return render_template('homepage.html', mensaje=mensaje)
    else:
        return render_template('logIn.html')


if __name__ == '__main__':
    uri = "neo4j+s://85d17210.databases.neo4j.io"
    user = "neo4j"
    password = "8_aBrbwezxsQxvPsIhl2UobQu-UQCH65zP6Da58Nplo"
    appNeo = App(uri, user, password)
    app.run()
    appNeo.close()
