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
    
    def createuser(self, Gender,Name,ids,Country,Age):
        query = """
        CREATE (u:user {
        Gender: $Gender,
        Name: $Name,
        ID: $ids,
        Country: $Country,
        Age: $Age
        })
        """

        with self.driver.session(database="neo4j") as session:
            session.run(query, Gender=Gender, Name=Name, ids=ids, Country=Country, Age=Age)
            

    #--- crear movie
    def createmovie(self,adult,genres,ids,language,company,datetime,title,vote_average):
        
        query = """
        CREATE (m:Movie {
        adult: $adult,
        genres: $genres,
        id: $ids,
        original_language: $language,
        production_companies: $company,
        release_date: $datetime,
        title: $title,
        vote_average: $vote_average
        })
        """
        
        with self.driver.session(database="neo4j") as session:
            session.run(query, adult=adult, genres=genres, ids=ids, language=language, company=company,
                    datetime=datetime, title=title, vote_average=vote_average)


    #--- crear staff
    def createstaff(self, Name, Gender,ids, Nationality, Rol, Email):
        query = """
        CREATE (p:staff {
        ID: $ids,
        Email: $Email,
        Gender: $Gender,
        Name: $Name,
        Nationality: $Nationality,
        Rol: $Rol
        })
        """
        
        with self.driver.session(database="neo4j") as session:
            session.run(query, ids=ids, Email=Email, Gender=Gender, Name=Name, Nationality=Nationality, Rol=Rol)
            print('se creo')
        
    #--- crear actor
    def createactor(self, Name, Profile_Path, Age,Gender, ids):
        query = """
        CREATE (a:actors {
        ID: $ids,
        Age: $Age,
        Gender: $Gender,
        Name: $Name,
        Profile_Path: $Profile_Path
        })
        """
        
        with self.driver.session(database="neo4j") as session:
            session.run(query, ids=ids, Age=Age, Gender=Gender, Name=Name, Profile_Path=Profile_Path)
                
    
    
    # ------------------------------------------------------ UPDATE -----------------------------------------
    
    #----------editarmovie
    
    #--pelicula
    def updatemovie(self,adult, genres, ids, language, company, datetime, title, vote_average):
        query = """
        MATCH (m:Movie {id: $ids})
        SET m.adult = $adult,
            m.genres = $genres,
            m.original_language = $language,
            m.production_companies = $company,
            m.release_date = $datetime,
            m.title = $title,
            m.vote_average = $vote_average
        """

        with self.driver.session(database="neo4j") as session:
            session.run(query, adult=adult, genres=genres, ids=ids, language=language, company=company,
                        datetime=datetime, title=title, vote_average=vote_average)
    
    #-- staff
    def updatestaff(self, ids,Email, Gender, Name, Nationality, Rol):
        query = """
        MATCH (p:staff {ID: $ids})
        SET p.Email = $Email,
            p.Gender = $Gender,
            p.Name = $Name,
            p.Nationality = $Nationality,
            p.Rol = $Rol
        """

        with self.driver.session(database="neo4j") as session:
            session.run(query, ids=ids, Email=Email, Gender=Gender, Name=Name, Nationality=Nationality, Rol=Rol)
        

    
    #-- actor
    def updateactor(self,gender,nombres,ids,profile,age):
        query = """
        MATCH (a:actors {ID: $ids})
        SET a.Gender = $gender, a.Name = $nombres, a.Profile_Path = $profile,
            a.Age = $age
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
    
    def updateuser(self, Gender, Name, ids, Country, Age):
        query = """
        MATCH (u:user {ID: $ids})
        SET u.Gender = $Gender,
            u.Name = $Name,
            u.Country = $Country,
            u.Age = $Age
        """

        with self.driver.session(database="neo4j") as session:
            session.run(query, Gender=Gender, Name=Name, ids=ids, Country=Country, Age=Age)

    
    #update html
    def update(self, label, old_property, old_value, new_property, new_value ):
        
        with self.driver.session(database="neo4j") as session:
            # Aquí puedes generar el query de actualización con los datos recibidos
            query = f"MATCH (n:{label}) WHERE n.{old_property} = '{old_value}' SET n.{new_property} = '{new_value}' RETURN n"
            result = session.run(query)
    # ------------------------------------------------------- START MOVIE ------------------------------------------------------- #

    def delete_movie_by_properties(self, properties):
        '''
            Eliminar una película dadas las propiedades.

            Parámetros
            ----------
            - properties: Diccionario de propiedades que filtrarán los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (m:Movie) WHERE "

            for key, value in properties.items():
                query += f"m.{key} = ${key} AND "

            query = query[:-4]
            query += "DETACH DELETE m"

            print(query)
            result = session.run(query, **properties)
            return result

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
                "DETACH DELETE m"
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

    def delete_actor_by_properties(self, properties):
        '''
            Eliminar un actor dadas las propiedades.

            Parámetros
            ----------
            - properties: Diccionario de propiedades que filtrarán los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (m:actors) WHERE "

            for key, value in properties.items():
                query += f"m.{key} = ${key} AND "

            query = query[:-4]
            query += "DETACH DELETE m"

            print(query)
            result = session.run(query, **properties)
            return result

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
                "DETACH DELETE m"
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

    def delete_staff_by_properties(self, properties):
        '''
            Eliminar un staff dadas las propiedades.

            Parámetros
            ----------
            - properties: Diccionario de propiedades que filtrarán los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (m:staff) WHERE "

            for key, value in properties.items():
                query += f"m.{key} = ${key} AND "

            query = query[:-4]
            query += "DETACH DELETE m"

            print(query)
            result = session.run(query, **properties)
            return result

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
                "DETACH DELETE m"
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
                "DETACH RETURN m"
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

    def delete_user_by_properties(self, properties):
        '''
            Eliminar un user dadas las propiedades.

            Parámetros
            ----------
            - properties: Diccionario de propiedades que filtrarán los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (m:user) WHERE "

            for key, value in properties.items():
                query += f"m.{key} = ${key} AND "

            query = query[:-4]
            query += "DETACH DELETE m"

            print(query)
            result = session.run(query, **properties)
            return result

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
                "DETACH DELETE m"
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

    
    def delete_platform_by_properties(self, properties):
        '''
            Eliminar una platform dadas las propiedades.

            Parámetros
            ----------
            - properties: Diccionario de propiedades que filtrarán los nodos a eliminar.

            Returns
            -------
            Validación.

        '''
        with self.driver.session(database="neo4j") as session:
            query = "MATCH (m:platform) WHERE "

            for key, value in properties.items():
                query += f"m.{key} = ${key} AND "

            query = query[:-4]
            query += "DETACH DELETE m"

            print(query)
            result = session.run(query, **properties)
            return result
    
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
                "DETACH DELETE m"
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

    def delete_mylist_relationship(self, user_id, movie_title):
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
        print(user_id)
        print(movie_title)
        with self.driver.session(database="neo4j") as session:
            query = (
                "MATCH (u:user {ID: $user_id})-[r:MyList]->(m:Movie {title: $movie_title}) "
                "DELETE r"
            )
            print(query)
            session.run(query, user_id=user_id, movie_title=movie_title)
    
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

    def find_mylist_by_user_property_return_movie(self, property_key, property_value):
        '''
            Obtener información de la película de la relación según propiedad del usuario.

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
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

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


    def agregarRelacion(self, pelicula_id,usuario_id,tipo):
        with self.driver.session(database="neo4j") as session:
            # Crear el query para agregar la relación
            query = f"""
                MATCH (p:Pelicula {{id: '{pelicula_id}'}}), (u:Usuario {{id: '{usuario_id}'}})
                CREATE (u)-[:{tipo}]->(p)
            """
            session.run(query)
        
    def delete_Favorites_relationship(self, user_id, movie_title):
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
                "MATCH (u:user {ID: $user_id})-[r:Favorites]->(m:Movie {title: $movie_title})"
                "DELETE r"
            )
            session.run(query, user_id=user_id, movie_title=movie_title)

    
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

    def find_Favorites_by_user_property_return_movie(self, property_key, property_value):
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
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

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

    def find_Available_In_by_platform_property_return_movie_info(self, property_key, property_value):
        '''
            Obtener información de la película de la relación según propiedad del usuario.

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
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

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

    def find_Subscribed_by_relationship_property_return_User(self, property_key, property_value):
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
                "RETURN u"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["u"] for record in result]
    
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

    # --------------------------------------------------- START Recommendation -------------------------------------------------- #
    def find_Recommendation_by_user_property_return_movie(self, property_key, property_value):
        '''
            Obtener información de la película de la relación según propiedad del usuario.

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
                "MATCH (u:user)-[r:Recommendation]->(m:Movie) "
                "WHERE u." + property_key + " = $" + property_key + " "
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #


    # ------------------------------------------------------ START Watched ------------------------------------------------------ #
    
    def find_Watched_by_user_property_return_movie(self, property_key, property_value):
        '''
            Obtener información de la película de la relación según propiedad del usuario.

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
                "RETURN m"
            )
            result = session.run(query, **{property_key: property_value})
            return [record["m"] for record in result]

    # --------------------------------------------------------------------------------------------------------------------------- #


    # -------------------------------------------------- START ejecución query -------------------------------------------------- #
    def execute_query(self, query):
        with self.driver.session(database="neo4j") as session:
            result = session.run(query)
            return result

    # --------------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    uri = "neo4j+s://85d17210.databases.neo4j.io"
    user = "neo4j"
    password = "8_aBrbwezxsQxvPsIhl2UobQu-UQCH65zP6Da58Nplo"
    app = App(uri, user, password)
    app.close()