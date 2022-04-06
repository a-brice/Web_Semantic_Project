from . import models
from .models import thread


domain = """
    PREFIX : <http://www.semanticweb.org/brice/ontologies/2022/2/TheOntology#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX ex: <http://www.example.com/>
    PREFIX ns: <http://www.w3.org/2003/06/sw-vocab-status/ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX wot: <http://xmlns.com/wot/0.1/>
    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX foaf: <http://xmlns.com/foaf/spec/#>
    PREFIX foaf1: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""



def get_json_obj(query_fn):
    thread.join()
    def func(*arg, **kw):
        query = domain + query_fn(*arg, **kw) 
        db = models.graph
        return db.query(query)
    return func




@get_json_obj
def query1():
    """
    List of all academies
    Name of all academies
    """
    return """ SELECT DISTINCT ?academy WHERE {
        ?academyId rdf:type :Academy .
        ?academyId foaf:name ?academy .
    } LIMIT 75
    """




@get_json_obj
def query2():
    """
    Name of all cities
    Cette requête peut servir pour compiler toutes les villes 
    disponibles et les mettre dans une combobox
    """
    return """ SELECT DISTINCT ?city WHERE {
            ?school rdf:type ?type .
            FILTER (?type = :Public || ?type = :Private)
            ?school :city ?city .
        } LIMIT 75
    """




@get_json_obj
def query3():
    """
    List of all ministries
    Name of all ministries
    """
    return """ SELECT DISTINCT ?ministry WHERE {
            ?ministryId rdf:type :Ministry .
            ?ministryId foaf:name ?ministry .
        } LIMIT 75
    """



@get_json_obj
def query5():
    """
    List of all schools
    Name, school, siret, type, category, latitude, longitude, 
    address, city, region, academy, ministry of all schools
    """
    return """ 
        SELECT DISTINCT ?name ?school ?tel ?siret 
          ?type ?category ?latitude ?longitude ?address 
          ?city ?region ?academy ?ministry WHERE {
            
            ?school rdf:type ?type .
            FILTER (?type = :Public || ?type = :Private)
            ?school foaf:name ?name .
            OPTIONAL {
                ?school :telephone ?tel .
            }
            OPTIONAL {
                ?school :siret ?siret .
            }
            OPTIONAL {
                ?school :schoolType ?category .
            }
            OPTIONAL {
                ?school :latitude ?latitude .
                ?school :longitude ?longitude .
            }
            OPTIONAL {
                ?school :address ?address .
            }
            OPTIONAL {
                ?school :city ?city .
            }
            OPTIONAL {
                ?school :region ?region .
            }
            OPTIONAL {
                ?school :hasAcademy ?academyI .
                ?academyI foaf:name ?academy .
            }
            OPTIONAL {
                ?school :hasMinistry ?ministryI .
                ?ministryI foaf:name ?ministry .
            }
        } LIMIT 30
    """



@get_json_obj
def query6(city_name='Paris'):
    """
    List of all schools located in a city
    Name, school, siret, type, category, latitude, longitude, 
    address, region, academy, ministry of all schools in the city of Paris. 
    To get the schools for another city, replace "Paris" by "name of the city"
    """
    return """ 
        SELECT DISTINCT ?name ?school ?tel 
          ?siret ?type ?category ?latitude ?longitude 
          ?address ?region ?academy ?ministry WHERE {

            ?school rdf:type ?type .
            FILTER (?type = :Public || ?type = :Private)
            ?school foaf:name ?name .
            ?school :city "%s" .
            OPTIONAL {
                ?school :telephone ?tel .
            }
            OPTIONAL {
                ?school :siret ?siret .
            }
            OPTIONAL {
                ?school :schoolType ?category .
            }
            OPTIONAL {
                ?school :latitude ?latitude .
                ?school :longitude ?longitude .
            }
            OPTIONAL {
                ?school :address ?address .
            }
            OPTIONAL {
                ?school :region ?region .
            }
            OPTIONAL {
                ?school :hasAcademy ?academyI .
                ?academyI foaf:name ?academy .
            }
            OPTIONAL {
                ?school :hasMinistry ?ministryI .
                ?ministryI foaf:name ?ministry .
            }
        }
    """ % city_name




@get_json_obj
def query7(wanted_age=50):
    """
    List of people older/younger than
    Name, age and position of people older than 50. 
    To get people older than age, replace 50 by wanted age. 
    To get people younger than age, replace > 50 by < wanted age.
    """
    return """
        SELECT DISTINCT ?individual ?age ?type WHERE {
            ?individual rdf:type ?type .
            FILTER (?type = :FullTime || ?type = :Apprentice || ?type = :Administrative || ?type = :IT || ?type = :Professor)
            ?individual foaf1:age ?age .
            FILTER (?age > %d)
        }
    """ % wanted_age




@get_json_obj
def query8(wanted_lower_age=20, wanted_upper_age=30):
    """
    List of people in a slice of age
    Name, age and position of people between 20  and 30. 
    To get people in another fork of age, 
    replace (?age >= 20 && ?age < 30) by 
    (?age >= wanted lower age && ?age < wanted upper age)
    """

    return """ 
        SELECT DISTINCT ?individual ?age ?type WHERE {
            ?individual rdf:type ?type .
            FILTER (?type = :FullTime || ?type = :Apprentice || ?type = :Administrative || ?type = :IT || ?type = :Professor)
            ?individual foaf1:age ?age .
            FILTER (?age >= %d && ?age < %d)
        }
    """ % (wanted_lower_age, wanted_upper_age)



@get_json_obj
def query9():
    """
    List of the instances of the geolocated POI
    Name, type, latitude and longitude of all schools 
    with registered latitude and longitude
    """
    return """
        SELECT DISTINCT ?school_UAI ?latitude ?longitude ?name WHERE {
            ?school_UAI rdf:type ?type .
            FILTER (?type = :Public || ?type = :Private)
            ?school_UAI :latitude ?latitude .
            ?school_UAI :longitude ?longitude .
            ?school_UAI foaf:name ?name .
        } LIMIT 150
    """



@get_json_obj
def query10():

    """
    List of all student 
    """
    return """
        SELECT DISTINCT ?individual ?type ?firstName ?lastName 
            ?age ?email ?nationality ?tel ?address ?city
        WHERE {
            ?individual rdf:type ?type .
            FILTER (?type = :FullTime || ?type = :Apprentice)
            ?individual foaf1:firstName ?firstName .
            ?individual foaf1:lastName ?lastName .

            OPTIONAL {
                ?individual foaf1:age ?age .
            }
            OPTIONAL {
                ?individual :email ?email .
            }
            OPTIONAL {
                ?individual :nationality ?nationality .
            }
            OPTIONAL {
                ?individual :telephone ?tel .
            }
            OPTIONAL {
                ?individual :address ?address .
            }
            OPTIONAL {
                ?individual :city ?city
            }
        }

    """


@get_json_obj
def query11():
    return """
        SELECT DISTINCT ?individual ?type ?firstName ?lastName 
            ?age ?email ?nationality ?tel ?address ?city
        WHERE {
            ?individual rdf:type ?type .
            FILTER (?type = :Administrative || ?type = :IT || ?type = :Professor)
            ?individual foaf1:firstName ?firstName .
            ?individual foaf1:lastName ?lastName .

            OPTIONAL {
                ?individual foaf1:age ?age .
            }
            OPTIONAL {
                ?individual :email ?email .
            }
            OPTIONAL {
                ?individual :nationality ?nationality .
            }
            OPTIONAL {
                ?individual :telephone ?tel .
            }
            OPTIONAL {
                ?individual :address ?address .
            }
            OPTIONAL {
                ?individual :city ?city
            }
        }

    """