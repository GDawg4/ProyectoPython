from neo4j import GraphDatabase, basic_auth

class Database(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    def write(self, _id, type, arguments):
        result = ""
        argumentsList = []
        if(type!=None):
            result += "CREATE (" + _id + ":" + type + ")\n"
            counter = 0
            for oneArgument in arguments:
                argumentsList.append(arguments[oneArgument])
                result += "SET " + _id + "." + oneArgument + " = $arguments[" + str(counter)  + "]" + "\n"
                counter += 1
        with self._driver.session() as session:
            session.write_transaction(self._crea, argumentsList, result)

    def connect(self, type1, type2, variableName1, variable1, VariableName2, variable2, linkName):
        result = "MATCH (a:" + type1 + "),(b:" + type2 + ")\nWHERE a." + variableName1 + "= $variable1 AND b." + VariableName2 + "= $variable2\nCREATE (a)-[:" + linkName + "]->(b)"
        with self._driver.session() as session:
            session.write_transaction(self._connect, result, variable1, variable2)

    def delete(self,nodeType,key,value):
        result = "MATCH (a:" + nodeType + ")\nWHERE a." + key + "= $value\nDETACH DELETE (a)"
        with self._driver.session() as session:
            session.write_transaction(self._delete,result,value)

    def deleteLink(self,type1,type2,variableName1,variable1,VariableName2,variable2,linkName):
        result = "MATCH (a:" + type1 + "),(b:" + type2 + ")\nWHERE a." + variableName1 + "= $variable1 AND b."+ VariableName2 + "= $variable2\nMATCH (a)-[r:"+linkName+"]->(b)\nDELETE r"
        with self._driver.session() as session:
            session.write_transaction(self._deleteLink,result,variable1,variable2)

    def upgrade(self,nodeType,key,value,newValue):
        result = "MATCH (a:" + nodeType + ")\nWHERE a." + key + "= $value\nSET a." + key + "= $newValue"
        with self._driver.session() as session:
            session.write_transaction(self._upgrade,result,value,newValue)

    def getNode(self,nodeType,key,value):
        result = "MATCH (a:" + nodeType + ")\nWHERE a." + key + "=$value\nRETURN a"
        with self._driver.session() as session:
            return session.write_transaction(self._getNode,result,value)

    def getNodesByOther(self,nodeType,key,value,link):
        result= "MATCH (a:" + nodeType + ")\nWHERE a." + key + "=$value\nMATCH (a)-[:" + link + "]->(m)<-[:" + link + "]-(r)\nRETURN r"
        with self._driver.session() as session:
            return session.write_transaction(self._getNodes,result,value)

    def getNodesByLink(self,nodeType,key,value,link):
        result= "MATCH (a:" + nodeType + ")\nWHERE a." + key + "=$value\nMATCH (a)-[:" + link + "]->(m)\nRETURN m"
        with self._driver.session() as session:
            return session.write_transaction(self._getNodes,result,value)

    def getAllType(self,nodeType):
        result= "MATCH (a:" + nodeType + ")\nRETURN a"
        with self._driver.session() as session:
            return session.write_transaction(self._Default,result)

    def getDefault(self):
        result = "MATCH (n) return n"
        with self._driver.session() as session:
            resultado = session.write_transaction(self._Default,result)
            return resultado
    def setDefault(self):
        if(self.getDefault().single() == None):
            result = """
            CREATE (Compu:Carrera{titulo:"Compu"})
            """
            with self._driver.session() as session:
                return session.write_transaction(self._Default,result)

    @staticmethod
    def _Default(tx, result):
        return tx.run(result)

    @staticmethod
    def _getNodes(tx, result, value):
        return tx.run(result, value)

    @staticmethod
    def _getNode(tx, result, value):
        return tx.run(result, value)

    @staticmethod
    def _upgrade(tx, result, value, newValue):
        result = tx.run(result, value, newValue)

    @staticmethod
    def _deleteLink(tx, result, variable1, variable2):
        result = tx.run(result, variable1, variable2)

    @staticmethod
    def _delete(tx, result, value):
        result = tx.run(result, value)

    @staticmethod
    def _connect(tx, result, variable1, variable2):
        result = tx.run(result, variable1, variable2)

    """This method is used by write"""

    @staticmethod
    def _create(tx, arguments, result):
        result = tx.run(result, arguments)