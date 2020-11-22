from owlready2 import *
from rdflib.graph import Graph
from .fetchData import main as fetch
from . import settings
import os

def deleteData(ontology, pid):
    """This function inserts data into the ontology.
        graph: type Graph
        description: hoot to the ontology
        request: type str
        description: sparql query
        return: None
    """
    world = World()
    world.get_ontology(ontology).load()
    graph = world.as_rdflib_graph()

    #if graph:
        #try:
            #with world.ontologies["dbo3.owl#"].load():
            #    graph.update(request)
        #except:
         #   print("Something went wrong:")
    #else:
        #print("Connection failed")
    try:
        destroy_entity((world.ontologies["dbo3.owl#"].load())["p" + str(pid)])
        world.save("dbo3.owl")
    except:
        print("Individual doesn't exist")
        return 0
    return 1

def main(pid):
    onto = "dbo3.owl"
    outcome = deleteData(onto, pid)
    return outcome

if __name__ == "__main__":
    main(1011)
