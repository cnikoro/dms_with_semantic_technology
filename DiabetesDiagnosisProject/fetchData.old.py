from owlready2 import *
from rdflib.graph import Graph

def connectOntology(ontology, endpoint=None):
    """This function connects to the ontology.
       ontology: type str
           description: The name of the saved local ontology
       endpoint: type str
           description: The endpoint to a remote ontology
       return type: graph
           description: returns rdf graph
    """
    world = World()
    world.get_ontology(ontology).load()
    graph = world.as_rdflib_graph()
    if graph:
        return graph
    else:
        print("connection failed")
        return

def getData(graph, request):
    """This function retrieves data from the ontolgy.
       graph: type Graph
           description: hook to the ontology
        request: type str
            description: sparql query
        return: data
           description: the list of data retrieved
    """
    results = list(graph.query(request))
    return results

def stripData(data):
    data = data.split('#')
    return data[1]

def main(attr, condition, val):
    """Main function calls connectOntology
       and getData functions to connect and
       retrieve data from ontology
    """
    data=dict()
    listOfData=list()
    PREFIX = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX : <http://www.semanticweb.org/user/ontologies/2020/5/untitled-ontology-30#>
        """
    FEATURES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]

    request = PREFIX + """
    SELECT ?numOfPreg ?glu ?bp ?skinThickness ?insulin ?bmi ?dpf ?age
        WHERE {{ 
        ?subject :hasID ?id; 
            :hasPregnancies ?numOfPreg;
            :hasGlucose ?glu;
            :hasBloodPressure ?bp;
            :hasSkinThickness ?skinThickness;
            :hasInsulin ?insulin;
            :hasBMI ?bmi;
            :hasDiabetesPedigreeFunction ?dpf;
            :hasAge ?age.
        FILTER({attr} {condition} {val}).
    }}
    """.format(attr=attr, condition=condition,  val=val)

    graph = connectOntology("dbo2.owl")
    if graph:
       results = getData(graph, request)
    else:
        print("Data could not be fetched")

    for result in results:
        for feature, row in zip(FEATURES, result):
            data[feature]=float(stripData(row))
            #print("{}: {}".format(feature, stripData(row)))
        listOfData.append(data)

    print((listOfData))
    return listOfData
if __name__ == "__main__":
    main("?id", "=", ":1")
