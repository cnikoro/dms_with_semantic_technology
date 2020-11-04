from owlready2 import *
from rdflib.graph import Graph
from .fetchData import main as fetch
from . import settings
import os

def update(ontology, request):
    """This function inserts data into the ontology.
       graph: type Graph
          description: hoot to the ontology
       request: type str
          description: sparql query
       return: None
    """

    world = World()
    world.get_ontology(ontology).load()
    #individual = (world.ontologies["dbo3.owl#"]).Patient(\
    #        "p" + str(pid), namespace=world.ontologies["dbo3.owl#"])
    graph = world.as_rdflib_graph()
    if graph:
        try:
            with world.ontologies["dbo3.owl#"].load():
                graph.update(request)
        except:
            print("Update could not be completed.")
    else:
        print("Connection failed")

    world.save(os.path.join(settings.BASE_DIR, "dbo3.owl"))

def main(feature, data, pid):
    """main(data) -> None
       Calls insertData to connect and insert data to Ontology
    """
    
    PREFIX = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX : <http://www.semanticweb.org/user/ontologies/2020/7/untitled-ontology-32#>
    """
    result = fetch("?id", "=", ":" + str(pid))
    onto = os.path.join(settings.BASE_DIR, "dbo3.owl")
    if len(result) != 0:
        if feature == "age":
            request = PREFIX + """
            DELETE
            {{
                ?patient :hasAge ?{feature}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid};
                         :hasAge ?{feature}.
            }}
            """.format(pid=pid, feature=feature)
            update(onto, request)
            
            request = PREFIX + """
            INSERT
            {{
                ?patient :hasAge :{data}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid}.
            }}
            """.format(data=data, pid=pid)
            
        elif feature == "bs":
            request = PREFIX + """
            DELETE
            {{
                ?patient :hasBloodSugar {feature}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid};
                         :hasBloodSugar {feature}.
            }}
            """.format(pid=pid, feature="?" + feature)
            update(onto, request)
            
            request = PREFIX + """
            INSERT
            {{
                ?patient :hasBloodSugar :{data}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid}.
            }}
            """.format(data=data, pid=pid)
        elif feature == "bp":
            request = PREFIX + """
            DELETE
            {{
                ?patient :hasBloodPressure {feature}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid};
                         :hasBloodPressure {feature}.
            }}
            """.format(pid=pid, feature="?" + feature)
            update(onto, request)
            
            request = PREFIX + """
            INSERT
            {{
                ?patient :hasBloodPressure :{data}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid}.
            }}
            """.format(data=data, pid=pid)
        elif feature == "pr":
            request = PREFIX + """
            DELETE
            {{
                ?patient :hasPlasmaR {feature}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid};
                         :hasPlasmaR {feature}.
            }}
            """.format(pid=pid, feature="?" + feature)
            update(onto, request)
            
            request = PREFIX + """
            INSERT
            {{
                ?patient :hasPlasmaR :{data}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid}.
            }}
            """.format(data=data, pid=pid)
        elif feature == "pf":
            request = PREFIX + """
            DELETE
            {{
                ?patient :hasPlasmaF {feature}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid};
                         :hasPlasmaF {feature}.
            }}
            """.format(pid=pid, feature="?" + feature)
            update(onto, request)
                        
            request = PREFIX + """
            INSERT
            {{
                ?patient :hasPlasmaF :{data}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid}.
            }}
            """.format(data=data, pid=pid)
        elif feature == "hbalc":
            request = PREFIX + """
            DELETE
            {{
                ?patient :hasHBALC {feature}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid};
                         :hasHBALC {feature}.
            }}
            """.format(pid=pid, feature="?" + feature)
            update(onto, request)
            
            request = PREFIX + """
            INSERT
            {{
                ?patient :hasHBALC :{data}.
            }}
            WHERE
            {{
                ?patient :hasID :{pid}.
            }}
            """.format(data=data, pid=pid)
        else:
            print("Unknown feature specified")
            return 0
    else:
        print("ID doesn't exist")
        return 0

    update(onto, request)
    return 1

if __name__ == "__main__":
    data = 21
    feature = "age"
    pid = 1011
    main(feature, data, pid)



