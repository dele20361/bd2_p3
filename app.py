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

@app.route('/crear_nodo', methods=['POST'])
def crear_nodo():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud POST

    # Extraer los valores necesarios para crear el nodo y las etiquetas
    nodo = data.get('nodo')
    labels = data.get('labels')

    # Verificar si los datos necesarios están presentes en la solicitud
    if not nodo or not labels:
        return 'Faltan datos requeridos', 400

    with driver.session() as session:
        # Crear el nodo con sus etiquetas
        labels_str = ':'.join(labels)  # Concatenar las etiquetas con ":" como separador
        query = (
            f"CREATE (n:{labels_str}) "
            f"SET n = $props "
            "RETURN n"
        )
        result = session.run(query, props=nodo)

        # Obtener el nodo recién creado
        created_node = result.single()[0]

        return str(created_node), 201

@app.route('/crear_relacion', methods=['POST'])
def crear_relacion():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud POST

    # Extraer los valores necesarios para crear la relación
    nodo_origen_id = data.get('nodo_origen_id')
    nodo_destino_id = data.get('nodo_destino_id')
    tipo_relacion = data.get('tipo_relacion')
    propiedades = data.get('propiedades')

    # Verificar si los datos necesarios están presentes en la solicitud
    if not nodo_origen_id or not nodo_destino_id or not tipo_relacion:
        return 'Faltan datos requeridos', 400

    with driver.session() as session:
        # Crear la relación con propiedades entre los nodos
        query = (
            "MATCH (nodo_origen), (nodo_destino) "
            "WHERE id(nodo_origen) = $nodo_origen_id AND id(nodo_destino) = $nodo_destino_id "
            "CREATE (nodo_origen)-[relacion:`" + tipo_relacion + "`]->(nodo_destino) "
            "SET relacion = $props "
            "RETURN relacion"
        )
        result = session.run(query, nodo_origen_id=nodo_origen_id, nodo_destino_id=nodo_destino_id, props=propiedades)

        # Obtener la relación recién creada
        created_relacion = result.single()[0]

        return str(created_relacion), 201

@app.route('/actualizar_nodo', methods=['POST'])
def actualizar_nodo():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud POST

    # Extraer los valores necesarios para la actualización del nodo
    where_propiedad = data.get('where_propiedad')
    where_valor = data.get('where_valor')
    propiedades_actualizar = data.get('propiedades_actualizar')

    # Verificar si los datos necesarios están presentes en la solicitud
    if not where_propiedad or not where_valor or not propiedades_actualizar:
        return 'Faltan datos requeridos', 400

    with driver.session() as session:
        # Actualizar el nodo con las propiedades especificadas
        query = (
            "MATCH (n) "
            f"WHERE n.{where_propiedad} = $where_valor "
            "SET "
        )

        propiedades_cypher = []
        for propiedad, valor in propiedades_actualizar.items():
            query += f"n.{propiedad} = ${propiedad}, "
            propiedades_cypher.append({propiedad: valor})

        query = query.rstrip(", ") + " RETURN n"

        result = session.run(query, **propiedades_cypher)

        # Obtener el nodo actualizado
        updated_node = result.single()[0]

        return str(updated_node), 200
@app.route('/editMovie')
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
