from flask import Flask, render_template, request, redirect, url_for
from system import App

app = Flask(__name__, template_folder='template', static_folder='static')

global_platform_name = ""

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

@app.route('/platform_selected', methods=['POST'])
def platform_selected():
    global global_platform_name
    platform_name = request.form['platformName']
    global_platform_name = platform_name
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contra = request.form['contra']
        
        # Validar el inicio de sesión
        result = appNeo.find_Subscribed_by_relationship_property(property_key='email', property_value=correo)
        if len(result) > 0:
            if result[0]['contra'] == contra:
                global userID
                userInfo = appNeo.find_Subscribed_by_relationship_property_return_User('email', correo)
                userID = userInfo[0]['ID']

                return redirect(url_for('homepage'))
        else:
            return redirect(url_for('login'))
        
    else:
        return render_template('logIn.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    # Obtener contenido de plataforma
    moviesContent = appNeo.find_Available_In_by_platform_property_return_movie_info('name', global_platform_name)
    titlesContent = [i['title'] for i in moviesContent]
    while len(titlesContent) < 20:
        titlesContent.append('...')
    if len(titlesContent) > 20:
        titlesContent = titlesContent[:20]

    # Obtener My List del user
    myListContent = appNeo.find_mylist_by_user_property_return_movie('ID', userID)
    myListContentTitles = [i['title'] for i in myListContent]
    while len(myListContentTitles) < 5:
        myListContentTitles.append('...')
    if len(myListContentTitles) > 5:
        myListContentTitles = myListContentTitles[:5]
    
    # Obtener Recomendaciones del user
    myRecos = appNeo.find_Recommendation_by_user_property_return_movie('ID', userID)
    myRecosTitles = [i['title'] for i in myRecos]
    while len(myRecosTitles) < 5:
        myRecosTitles.append('...')
    if len(myRecosTitles) > 5:
        myRecosTitles = myRecosTitles[:5]

    # Obtener Favorites
    favoritesContent = appNeo.find_Favorites_by_user_property_return_movie('ID', userID)
    favoritesTitles = [i['title'] for i in favoritesContent]
    while len(favoritesTitles) < 5:
        favoritesTitles.append('...')
    if len(favoritesTitles) > 5:
        favoritesTitles = favoritesTitles[:5]

    return render_template('homepage.html', titlesContent=titlesContent, myListContentTitles=myListContentTitles, myRecosTitles=myRecosTitles, favoritesTitles=favoritesTitles)

@app.route('/editMovie', methods=['GET', 'POST'])
def editMovie():
    return render_template('editarMovie.html')

@app.route('/editUser', methods=['GET', 'POST'])
def editUser():
    return render_template('editarUser.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    return render_template('consulta.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
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

    # email: 
    # osborncolleen@example.org

    # contra: 
    # (Gn3NTag2B