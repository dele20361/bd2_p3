import logging

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    #------------------------------------------------------- CREATE
    
    #--- user
    
    def createuser(self, gender,name,ids,country,age):
        query = """
        CREATE (u:User {name: $name, country: $country, id: $ids, age: $age, gender: $gender})
        """

        parameters = {
            'name': name,
            'country': country,
            'ids': ids,
            'age': age,
            'gender': gender
        }

        with self.driver.session(database="neo4j") as session:
            result = session.run(query, parameters)

    
    # ------------------------------------------------------ UPDATE -----------------------------------------
    
    #----------editarmovie
    
    #--pelicula
    def updatemovie(self,adult,genres,ids,Lenguage, nombres, datetime,tittle,vote_average):
        query = """
        MATCH (m:Movie {id: $ids})
        SET m.adult = $adult, m.genres = $genres, m.lenguage = $lenguage,
            m.nombres = $nombres, m.datetime = $datetime, m.tittle = $tittle,
            m.vote_average = $vote_average
        """

        parameters = {
            'ids': ids,
            'adult': adult,
            'genres': genres,
            'lenguage': Lenguage,
            'nombres': nombres,
            'datetime': datetime,
            'tittle': tittle,
            'vote_average': vote_average
        }

        with self.driver.session(database="neo4j") as session:
            result = session.run(query, parameters)
    
    #-- staff
    def updatestaff(self, gender,nombres,ids,nationality,rol,correo):
        query = """
        MATCH (s:Staff {id: $ids})
        SET s.gender = $gender, s.nombres = $nombres, s.nationality = $nationality,
            s.rol = $rol, s.correo = $correo
        """

        parameters = {
            'ids': ids,
            'gender': gender,
            'nombres': nombres,
            'nationality': nationality,
            'rol': rol,
            'correo': correo
        }

        with self.driver.session(database="neo4j") as session:
            result = session.run(query, parameters)
    

    
    #-- actor
    def updateactor(self,gender,nombres,ids,profile,age):
        query = """
        MATCH (a:Actor {id: $ids})
        SET a.gender = $gender, a.nombres = $nombres, a.profile = $profile,
            a.age = $age
        """

        parameters = {
            'ids': ids,
            'gender': gender,
            'nombres': nombres,
            'profile': profile,
            'age': age
        }

        with self.driver.session(database="neo4j") as session:
            result = session.run(query, parameters)

    #------------------ update user
    
    def updateuser(self, gender,name,ids,country,age):
        query = """
        MATCH (u:User {id: $ids})
        SET u.name = $name, u.country = $country, u.age = $age, u.gender = $gender
        """

        parameters = {
            'ids': ids,
            'name': name,
            'country': country,
            'age': age,
            'gender': gender
        }

        with self.driver.session(database="neo4j") as session:
            result = session.run(query, parameters)

    
    #update html
    def update(self, label, old_property, old_value, new_property, new_value ):
        
        with self.driver.session(database="neo4j") as session:
            # Aquí puedes generar el query de actualización con los datos recibidos
            query = f"MATCH (n:{label}) WHERE n.{old_property} = '{old_value}' SET n.{new_property} = '{new_value}' RETURN n"
            result = session.run(query)
    # ------------------------------------------------------- START MOVIE ------------------------------------------------------- #

    def delete_movie_by_property(self, property_key, property_value):
        '''
            Eliminar una película dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "DELETE m"
            )
            result = session.run(query, **{property_key: property_value})
            return result
    
    def find_movie_by_property(self, property_key, property_value):
        '''
            Buscar una película dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos.
            - property_value: Valor de la propiedad que filtrará los nodos.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record['m'] for record in result]
    
    def find_movies(self):
        '''
            Buscar todas las películas.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie) "
                "RETURN m"
            )
            result = session.run(query)
            return [record['m'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #
    
    # ------------------------------------------------------- START ACTOR ------------------------------------------------------- #

    def delete_actor_by_property(self, property_key, property_value):
        '''
            Eliminar una actor dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:actors) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "DELETE m"
            )
            result = session.run(query, **{property_key: property_value})
            return result
    
    def find_actor_by_property(self, property_key, property_value):
        '''
            Buscar una actor dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos.
            - property_value: Valor de la propiedad que filtrará los nodos.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:actors) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

    def find_actors(self):
        '''
            Buscar todos los actores.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:actors) "
                "RETURN m"
            )
            result = session.run(query)
            return [record['m'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #
    
    # ------------------------------------------------------- START STAFF ------------------------------------------------------- #

    def delete_staff_by_property(self, property_key, property_value):
        '''
            Eliminar un staff dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:staff) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "DELETE m"
            )
            result = session.run(query, **{property_key: property_value})
            return result
    
    def find_staff_by_property(self, property_key, property_value):
        '''
            Buscar un staff dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos.
            - property_value: Valor de la propiedad que filtrará los nodos.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:staff) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

    def find_staff(self):
        '''
            Buscar todos los nodos staff.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:staff) "
                "RETURN m"
            )
            result = session.run(query)
            return [record['m'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #
    
    # -------------------------------------------------------  START USER ------------------------------------------------------- #

    def delete_user_by_property(self, property_key, property_value):
        '''
            Eliminar un user dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:user) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "DELETE m"
            )
            result = session.run(query, **{property_key: property_value})
            return result
    
    def find_user_by_property(self, property_key, property_value):
        '''
            Buscar un user dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos.
            - property_value: Valor de la propiedad que filtrará los nodos.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:user) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

    def find_users(self):
        '''
            Buscar todos los nodos staff.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:user) "
                "RETURN m"
            )
            result = session.run(query)
            return [record['m'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #
    
    # ----------------------------------------------------- START PLATFORM ------------------------------------------------------ #

    def delete_platform_by_property(self, property_key, property_value):
        '''
            Eliminar un platform dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:platform) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "DELETE m"
            )
            result = session.run(query, **{property_key: property_value})
            return result
    
    def find_platform_by_property(self, property_key, property_value):
        '''
            Buscar un platform dada una key.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos.
            - property_value: Valor de la propiedad que filtrará los nodos.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:platform) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

    def find_platform(self):
        '''
            Buscar todos los nodos platform.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:platform) "
                "RETURN m"
            )
            result = session.run(query)
            return [record['m'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #
    
    # ------------------------------------------------------ START MyList ------------------------------------------------------- #

    def delete_mylist_relationship(self, user_id, movie_id):
        '''
            Eliminar relación MyList entre user y movie.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user {id: $user_id})-[r:MyList]->(m:Movie {id: $movie_id}) "
                "DELETE r"
            )
            session.run(query, user_id=user_id, movie_id=movie_id)

    
    def find_mylist_by_relationship_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la relación.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:MyList]->(m:Movie) "
                "WHERE r." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_mylist_by_movie_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la película.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:MyList]->(m:Movie) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_mylist_by_user_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad del usuario.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:MyList]->(m:Movie) "
                "WHERE u." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]

    def find_myList(self):
        '''
            Buscar relaciones "My List".

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:MyList]->(m:Movie)  "
                "RETURN r"
            )
            result = session.run(query)
            return [record['r'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------------------- START Favorites ----------------------------------------------------- #

    def delete_Favorites_relationship(self, user_id, movie_id):
        '''
            Eliminar relación Favorites entre user y movie.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user {id: $user_id})-[r:Favorites]->(m:Movie {id: $movie_id}) "
                "DELETE r"
            )
            session.run(query, user_id=user_id, movie_id=movie_id)

    
    def find_Favorites_by_relationship_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la relación.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Favorites]->(m:Movie) "
                "WHERE r." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Favorites_by_movie_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la película.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Favorites]->(m:Movie) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Favorites_by_user_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad del usuario.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Favorites]->(m:Movie) "
                "WHERE u." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]

    def find_Favorites(self):
        '''
            Buscar relaciones "Favorites".

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Favorites]->(m:Movie)  "
                "RETURN r"
            )
            result = session.run(query)
            return [record['r'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------------------- START Watched ----------------------------------------------------- #

    def delete_Watched_relationship(self, user_id, movie_id):
        '''
            Eliminar relación Watched entre user y movie.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user {id: $user_id})-[r:Watched]->(m:Movie {id: $movie_id}) "
                "DELETE r"
            )
            session.run(query, user_id=user_id, movie_id=movie_id)

    
    def find_Watched_by_relationship_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la relación.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Watched]->(m:Movie) "
                "WHERE r." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Watched_by_movie_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la película.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Watched]->(m:Movie) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Watched_by_user_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad del usuario.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Watched]->(m:Movie) "
                "WHERE u." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]

    def find_Watched(self):
        '''
            Buscar relaciones "Watched".

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Watched]->(m:Movie)  "
                "RETURN r"
            )
            result = session.run(query)
            return [record['r'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------------------- START Rating ----------------------------------------------------- #

    def delete_Rating_relationship(self, user_id, movie_id):
        '''
            Eliminar relación Rating entre user y movie.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user {id: $user_id})-[r:Rating]->(m:Movie {id: $movie_id}) "
                "DELETE r"
            )
            session.run(query, user_id=user_id, movie_id=movie_id)

    
    def find_Rating_by_relationship_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la relación.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Rating]->(m:Movie) "
                "WHERE r." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Rating_by_movie_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la película.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Rating]->(m:Movie) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Rating_by_user_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad del usuario.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Rating]->(m:Movie) "
                "WHERE u." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]

    def find_Rating(self):
        '''
            Buscar relaciones "Rating".

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Rating]->(m:Movie)  "
                "RETURN r"
            )
            result = session.run(query)
            return [record['r'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------------------- START Available_In ----------------------------------------------------- #

    def delete_Available_In_relationship(self, movie_id, platform_id):
        '''
            Eliminar relación Available_In entre movie y platform.

            Parámetros
            ----------
            - movie_id: Id de película
            - platform_id: Id de plataforma.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie {id: $movie_id})-[r:Available_In]->(p:platform {id: $platform_id}) "
                "DELETE r"
            )
            session.run(query, movie_id=movie_id, platform_id=platform_id)

    
    def find_Available_In_by_relationship_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la relación.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie)-[r:Available_In]->(p:platform) "
                "WHERE r." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Available_In_by_movie_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la película.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie)-[r:Available_In]->(p:platform) "
                "WHERE m." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Available_In_by_platform_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad del usuario.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie)-[r:Available_In]->(p:platform) "
                "WHERE p." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]

    def find_Available_In(self):
        '''
            Buscar relaciones "Available_In".

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (m:Movie)-[r:Available_In]->(p:platform) "
                "RETURN r"
            )
            result = session.run(query)
            return [record['r'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------------------- START Subscribed ----------------------------------------------------- #

    def delete_Subscribed_relationship(self, user_id, platform_id):
        '''
            Eliminar relación Subscribed entre user y platform.

            Parámetros
            ----------
            - user_id: Id del user.
            - platform_id: Id de la plataforma.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user {id: $user_id})-[r:Subscribed]->(p:platform {id: $platform_id}) "
                "DELETE r"
            )
            session.run(query, user_id=user_id, platform_id=platform_id)

    
    def find_Subscribed_by_relationship_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la relación.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Subscribed]->(p:platform) "
                "WHERE r." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Subscribed_by_platform_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la película.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Subscribed]->(p:platform) "
                "WHERE p." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Subscribed_by_user_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad del usuario.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Subscribed]->(p:platform) "
                "WHERE u." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]

    def find_Subscribed(self):
        '''
            Buscar relaciones "Subscribed".

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Subscribed]->(p:platform)  "
                "RETURN r"
            )
            result = session.run(query)
            return [record['r'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #

    # ----------------------------------------------------- START Acted_in ------------------------------------------------------ #

    def delete_Acted_in_relationship(self, user_id, platform_id):
        '''
            Eliminar relación Acted_in entre actor y movie.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user {id: $user_id})-[r:Acted_in]->(p:platform {id: $platform_id}) "
                "DELETE r"
            )
            session.run(query, user_id=user_id, platform_id=platform_id)

    
    def find_Acted_in_by_relationship_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la relación.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Acted_in]->(p:platform) "
                "WHERE r." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Acted_in_by_platform_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad de la película.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Acted_in]->(p:platform) "
                "WHERE p." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]
    
    def find_Acted_in_by_user_property(self, property_key, property_value):
        '''
            Obtener información de la relación según propiedad del usuario.

            Parámetros
            ----------
            - property_key: Nombre de la propiedad que filtrará los nodos a eliminar.
            - property_value: Valor de la propiedad que filtrará los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Acted_in]->(p:platform) "
                "WHERE u." + property_key + " = $" + property_key + " "
                "RETURN r"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["r"] for record in result]

    def find_Acted_in(self):
        '''
            Buscar relaciones "Acted_in".

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user)-[r:Acted_in]->(p:platform)  "
                "RETURN r"
            )
            result = session.run(query)
            return [record['r'] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #

    # -------------------------------------------------- START ejecución query -------------------------------------------------- #
    def execute_query(self, query):
        with self.driver.session(database="neo4j") as session:
            result = session.run(query)
            return result

if __name__ == "__main__":
    uri = "neo4j+s://85d17210.databases.neo4j.io"
    user = "neo4j"
    password = "8_aBrbwezxsQxvPsIhl2UobQu-UQCH65zP6Da58Nplo"
    app = App(uri, user, password)
    # app.create_friendship("Alice", "David")
    # result = app.find_movie_by_property('title', 'Toy Story')
    # result = app.delete_movie_by_property('title', 'Toy Waiting to Exhale')

    # deletedMovie = {
    #     'original_language': "en",
    #     'release_date': '1995-12-22T00:00:00Z',
    #     'production_companies': "[{'name': 'Twentieth Century Fox Film Corporation', 'id': 306}]",
    #     'genres': "[{'id': 35, 'name': 'Comedy'}, {'id': 18, 'name': 'Drama'}, {'id': 10749, 'name': 'Romance'}]",
    #     'vote_average': 6.1,
    #     'id': 31357,
    #     'title': "Waiting to Exhale",
    #     'adult': False
    # }

    # result = app.find_actor_by_property('Name', 'Melinda West')
    result = app.find_myList()
    node = result[0]
    # print(node.keys())
    print(len(result))
    # print(node)
    # for i in result[0]:
    #     print(i + '\n')
    app.close()