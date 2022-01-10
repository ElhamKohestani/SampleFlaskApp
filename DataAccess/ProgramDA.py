
from DataAccess.DataConnection import DbConnection

class Program:
    def __init__(self, abbreviation = None, identifier = None, id = None):
        self.abbreviation = abbreviation
        self.identifier = identifier
        self.id = id
        self._dbCon = DbConnection()

    def getProgram(self, id = None):

        query  =  "select * from look.Program where ID = ?" if id != None else "select * from look.Program"

        result = self._dbCon._cursor.execute(query)
        return result

