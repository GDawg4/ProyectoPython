from Database import *

class Project():
    def __init__(self):
        self.db = Database("bolt://localhost:7687", "neo4j","password")
        self.db.setDefault()

    def getAllCareers(self):
        allCareers = []
        careersFromDatabase = self.db.getAllType("Carrera")
        print(type(careersFromDatabase))
        for career in careersFromDatabase:
            allCareers.append(career)
        return allCareers