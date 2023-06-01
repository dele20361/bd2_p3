from flask import Flask, render_template, request, redirect, url_for
from dateutil import parser
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
        
@app.route('/agregarRelacion', methods=['POST'])
def agregarRelacion():
    # Obtener el ID de la película y el ID del usuario en sesión desde los datos enviados por POST
    data = request.get_json()
    destino = data['destino']
    titlecontent = data['titlecontent']
    usuario_id=userID

    # Realiza alguna acción con los datos recibidos

    appNeo.agregarRelacion(destino,usuario_id,titlecontent)
    



    # Obtener My List del user
    myListContent = appNeo.find_mylist_by_user_property_return_movie('ID', userID)
    myListContentTitles = [i['title'] for i in myListContent]
    while len(myListContentTitles) < 5:
        myListContentTitles.append('...')
    if len(myListContentTitles) > 5:
        myListContentTitles = myListContentTitles[-5:]
    
    # Obtener Recomendaciones del user
    myRecos = appNeo.find_Recommendation_by_user_property_return_movie('ID', userID)
    myRecosTitles = [i['title'] for i in myRecos]
    while len(myRecosTitles) < 5:
        myRecosTitles.append('...')
    if len(myRecosTitles) > 5:
        myRecosTitles = myRecosTitles[-5:]

    # Obtener Favorites
    favoritesContent = appNeo.find_Favorites_by_user_property_return_movie('ID', userID)
    favoritesTitles = [i['title'] for i in favoritesContent]
    while len(favoritesTitles) < 5:
        favoritesTitles.append('...')
    if len(favoritesTitles) > 5:
        favoritesTitles = favoritesTitles[-5:]

    # Obtener Watched
    watched = appNeo.find_Watched_by_user_property_return_movie('ID', userID)
    watchedTitles = [i['title'] for i in watched]
    while len(watchedTitles) < 5:
        watchedTitles.append('...')
    if len(watchedTitles) > 5:
        watchedTitles = watchedTitles[-5:]

    return render_template('homepage.html', titlesContent=titlesContent, myListContentTitles=myListContentTitles, myRecosTitles=myRecosTitles, favoritesTitles=favoritesTitles, watchedTitles=watchedTitles)

@app.route('/deleteMyFavorites', methods=['GET', 'POST'])
def deleteMyFavorites():
    if request.method == 'POST':
        favoritesTitle = request.form['favoritesTitle']
        print(favoritesTitle)
        
        # Eliminar relación
        appNeo.delete_Favorites_relationship(userID, favoritesTitle)
        return redirect(url_for('homepage'))

@app.route('/deleteMyList', methods=['GET', 'POST'])
def deleteMyList():
    if request.method == 'POST':
        myListTitle = request.form['myListTitle']
        
        # Eliminar relación
        appNeo.delete_mylist_relationship(userID, myListTitle)
        return redirect(url_for('homepage'))

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
            date_str = request.form['datetime']
            title = request.form['title']
            vote_average = request.form['vote_average']

            # Casting a tipo de dato correcto
            ids = int(ids)
            adult = bool(adult)
            vote_average = float(vote_average)
            
            parsed_date = parser.isoparse(date_str)
            timestamp = parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Ejecutar el query de creación de película en la base de datos
            appNeo.createmovie(adult, genres, ids, language, company, timestamp, title, vote_average)
            
        elif request.form['submit'] == 'Crear Staff':
            # Lógica para crear un miembro del staff en la base de datos
            # Extraer los datos del formulario
            nombres = request.form['nombresS']
            gender = request.form['gender']
            ids = request.form['idsS']
            nationality = request.form['nationality']
            rol = request.form['rol']
            correo = request.form['correo']

            # Casting a tipo de dato correcto
            print(ids)
            print(type(ids))
            ids = int(ids)
            gender = int(gender)

            # Ejecutar el query de creación de miembro del staff en la base de datos
            appNeo.createstaff(nombres, gender, ids, nationality, rol, correo)
                   
        elif request.form['submit'] == 'Crear Actor':
            # Lógica para crear un actor en la base de datos
            # Extraer los datos del formulario
            nombres = request.form['nombresA']
            profile = request.form['profile']
            age = request.form['age']
            gender = request.form['genderA']
            ids = request.form['ids']

            # Casting a tipo de dato correcto
            ids = int(ids)
            gender = int(gender)
            age = int(age)

            # Ejecutar el query de creación de actor en la base de datos
            appNeo.createactor(nombres, profile, age, gender, ids)
            
        elif request.form['submit'] == 'Eliminar Pelicula':
            # Lógica para realizar la eliminación en la base de datos
            adult = request.form['adult']
            genres = request.form['genres']
            ids = request.form['ids']
            language = request.form['lenguage']
            company = request.form['nombres']
            datetime = request.form['datetime']
            title = request.form['title']
            vote_average = request.form['vote_average']
            
            toEval = {'adult':adult, 'genres':genres, 'id':ids, 'original_language':language, 'production_companies':company, 'release_date':datetime, 'title':title, 'vote_average':vote_average}
            
            # Obtener propiedades que tengan contenido
            non_empty_properties = {key: value for key, value in toEval.items() if value}
            non_empty_dict = {key: non_empty_properties[key] for key in non_empty_properties}

            # Cast al tipo de dato correcto
            keys = non_empty_dict.keys()
            if 'adult' in keys:
                non_empty_dict['adult'] = bool(non_empty_dict['adult'])
            if 'release_date' in keys:
                non_empty_dict['release_date'] = datetime.fromisoformat(non_empty_dict['release_date'])
            if 'id' in keys:
                non_empty_dict['id'] = int(non_empty_dict['id'])
            if 'vote_average' in keys:
                non_empty_dict['vote_average'] = float(non_empty_dict['vote_average'])
            
            if len(keys) > 0:
                appNeo.delete_movie_by_properties(non_empty_dict)

        elif request.form['submit'] == 'Eliminar Staff':
            # Lógica para realizar la eliminación en la base de datos
            nombres = request.form['nombresS']
            gender = (request.form['gender'])
            ids = (request.form['idsS'])
            nationality = request.form['nationality']
            rol = request.form['rol']
            correo = request.form['correo']

            toEval = {'Name': nombres, 'Gender': gender, 'ID': ids, 'Nationality': nationality, 'Rol': rol, 'Email': correo}

            # Obtener propiedades que tengan contenido
            non_empty_properties = {key: value for key, value in toEval.items() if value}
            non_empty_dict = {key: non_empty_properties[key] for key in non_empty_properties}

            # Cast al tipo de dato correcto
            keys = non_empty_dict.keys()
            if 'ID' in keys:
                non_empty_dict['ID'] = int(non_empty_dict['ID'])
            if 'Gender' in keys:
                non_empty_dict['Gender'] = int(non_empty_dict['Gender'])

            if len(keys) > 0:
                appNeo.delete_staff_by_properties(non_empty_dict)

        elif request.form['submit'] == 'Eliminar Actor':
            # Lógica para realizar la eliminación en la base de datos
            nombres = request.form['nombresA']
            profile = request.form['profile']
            age = request.form['age']
            gender = request.form['genderA']
            ids = request.form['ids']

            toEval = {'Name': nombres, '`Profile Path`': profile, 'Age': age, 'Gender': gender, 'ID': ids}

            print(toEval)
            # Obtener propiedades que tengan contenido
            non_empty_properties = {key: value for key, value in toEval.items() if value}
            non_empty_dict = {key: non_empty_properties[key] for key in non_empty_properties}

            # Cast al tipo de dato correcto
            keys = non_empty_dict.keys()
            if 'ID' in keys:
                non_empty_dict['ID'] = int(non_empty_dict['ID'])
            if 'Gender' in keys:
                non_empty_dict['Gender'] = int(non_empty_dict['Gender'])
            
            print(non_empty_dict)

            if len(keys) > 0:
                appNeo.delete_actor_by_properties(non_empty_dict)
            else:
                print('VACIO')

        elif request.form['submit'] == 'Actualizar Pelicula':
            # Lógica para actualizar los datos de la película
            adult = request.form['adult']
            genres = request.form['genres']
            ids = request.form['ids']
            language = request.form['lenguage']
            company = request.form['nombres']
            date_str = request.form['datetime']
            title = request.form['title']
            vote_average = request.form['vote_average']

            # Casting a tipo de datos correcto
            ids = int(ids)
            adult = bool(adult)
            vote_average = float(vote_average)

            parsed_date = parser.isoparse(date_str)
            timestamp = parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            appNeo.updatemovie(adult, genres, ids, language, company, timestamp, title, vote_average)
            
        elif request.form['submit'] == 'Actualizar Staff':
            # Lógica para actualizar los datos del staff
            nombres = request.form['nombresS']
            gender = request.form['gender']
            ids = request.form['idsS']
            nationality = request.form['nationality']
            rol = request.form['rol']
            correo = request.form['correo']

            # Casting a tipo de dato correcto
            ids = int(ids)
            gender = int(gender)
            
            appNeo.updatestaff(ids, correo, gender, nombres, nationality, rol)
            
        elif request.form['submit'] == 'Actualizar Actor':
            # Lógica para actualizar los datos del actor
            nombres = request.form['nombresA']
            profile = request.form['profile']
            age = request.form['age']
            gender = request.form['genderA']
            ids = request.form['ids']

            # Casting a tipo de dato correcto
            ids = int(ids)
            gender = int(gender)
            age = int(age)
            
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
            name = request.form['name']
            country = request.form['country']
            ids = request.form['ids']
            age = request.form['age']
            gender = request.form['gender']

            toEval = {'Name': name, 'Age': age, 'Gender': gender, 'ID': ids, 'Country': country}

            # Obtener propiedades que tengan contenido
            non_empty_properties = {key: value for key, value in toEval.items() if value}
            non_empty_dict = {key: non_empty_properties[key] for key in non_empty_properties}

            # Cast al tipo de dato correcto
            keys = non_empty_dict.keys()
            if 'ID' in keys:
                non_empty_dict['ID'] = int(non_empty_dict['ID'])
            if 'Age' in keys:
                non_empty_dict['Age'] = bool(non_empty_dict['Age'])
            if 'Gender' in keys:
                non_empty_dict['Gender'] = int(non_empty_dict['Gender'])
            
            print(non_empty_dict)

            if len(keys) > 0:
                appNeo.delete_user_by_properties(non_empty_dict)
            else:
                print('VACIO')


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
    return render_template('search.html', title='', info='')

@app.route("/searchMovie", methods=['GET', 'POST'])
def searchMovie():
    if request.method == 'POST':
        # Obtener contenido de plataforma
        moviesContent = appNeo.find_movies()
        titlesContent = [i['title'] for i in moviesContent]

        title = request.form['searchBar']

        if title in titlesContent:
            # Buscar info de película
            result = appNeo.find_movie_by_property('title', title)
            movieInfo = result[0]
            description = f"""
            - Idioma original: {movieInfo['original_language']}\n
            - Fecha de estreno: {(movieInfo['release_date'])}\n
            \n\n
            Puntuación: {movieInfo['vote_average']}
            """
            return render_template('search.html', title=title, info=description)
        else:
            return render_template('search.html', title='No se encontró el título en la base de datos.', info='')

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
    if request.method == 'POST':
        if request.form['submit'] == 'Crear':
            pass
        elif request.form['submit'] == 'Eliminar':
            ids = request.form['ids']
            name = request.form['name']
            available_in = request.form['available_in']
            founder = request.form['founder']
            image_link = request.form['image_link']
            profit = request.form['profit']

            toEval = {'id': ids, 'name': name, 'available_in': available_in, 'founder': founder, 'image_link': image_link, 'profit': profit}

            # Obtener propiedades que tengan contenido
            non_empty_properties = {key: value for key, value in toEval.items() if value}
            non_empty_dict = {key: non_empty_properties[key] for key in non_empty_properties}

            # Cast al tipo de dato correcto
            keys = non_empty_dict.keys()
            if 'id' in keys:
                non_empty_dict['id'] = int(non_empty_dict['id'])

            print(non_empty_dict)

            if len(keys) > 0:
                appNeo.delete_platform_by_properties(non_empty_dict)
            else:
                print('VACIO')

        elif request.form['submit'] == 'Actualizar':
            pass

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