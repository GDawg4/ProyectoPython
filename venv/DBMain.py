from neo4j import GraphDatabase
from Database import *
from Classes import *
from Project import Project

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def print_related_to(tx, name):
    for record in tx.run("MATCH (a:Clase)-[:lleva]->(f) "
                         "WHERE a.nombre = {name} "
                         "RETURN f.nombre", name=name):
        print(record["f.nombre"])

with driver.session() as session:
    session.read_transaction(print_related_to, "Química")

currentproject = Project()
for words in currentproject.getAllCareers():
    print(words)