from DataAccess.DataConnection import DbConnection

class Visitor:
    def __init__(self, registrationId = None, name =None, gender =None, graduationClass = None, registrationDate = None, lname = None, programs = None):
        self.registrationId = registrationId
        self.name = name
        self.gender = gender
        self.graduationClass = graduationClass
        self.registrationDate = registrationDate
        self.lname = lname
        self.programs = programs
        self._dbCon = DbConnection()


    def getRegistered(self, topRecords = None):
        query = "SELECT TOP " + ("10" if topRecords == None else str(topRecords)) +  " ID, [Name], LastName, IIF(Gender = '1', 'Male', IIF(Gender = '2', 'Female', 'No Gender')) as Gender, GraduationClass FROM st.Visitor SELECT TOP 10 ID, [Name], LastName, IIF(Gender = '1', 'Male', IIF(Gender = '2', 'Female', 'No Gender')) as Gender, GraduationClass FROM st.Visitor ORDER BY RegistrationDate DESC"
        
        return self._dbCon.executeSelect(query)


    def DeleteVisitor(self, regID):
        query = "DELETE FROM st.Visitor WHERE ID = ?"
        return self._dbCon.executeDelete(query, paramters= (regID,))

    #get a registered visitor along with its programs.
    def getVisitorPrograms(self, id):
        query = "SELECT ProgramID FROM st.VisitorProgram WHERE VisitorID = ? "
        programs = self._dbCon.executeSelect(query, (id,))

        program_list = []
        #changing list of tuples to list of list
        list_of_visitor_programs = [list(elem) for elem in programs]
        
        for subArr in list_of_visitor_programs:
            program_list.append(subArr[0])

        return program_list
        
    def getVisitor(self, id):
        query = """SELECT ID, [Name], LastName,  Gender, GraduationClass FROM st.Visitor
                    WHERE ID = ?"""
        result = self._dbCon.executeSelect(query,  (id,))
        

        return (result)

        
    def registerVisitor(self):

        query = ""
        params = ()
        if self.registrationId !=None and self.registrationId !="":
            query = """
            EXECUTE  [st].[UpdateVisitor] 
                        @RegID = ?,
                        @FirstName = ?,
                        @LastName = ?,
                        @GraduationClass = ?,
                        @Gender	= ?,
                        @Programs = ?
                                """
            params = (self.registrationId, self.name, self.lname , self.graduationClass, self.gender, self.programs)
        
        else:
            query = """
            DECLARE	
            @OutRegID nvarchar(60)

            EXEC	 [st].[RegistorVisitor]
            @FirstName = ?,
            @LastName = ?,
            @GraduationClass = ?,
            @Gender = ?,
            @Programs = ?,
            @OutRegID = @OutRegID OUTPUT

            SELECT	@OutRegID as N'@OutRegID'
                                """   
            params = (self.name, self.lname , self.graduationClass, self.gender, self.programs) 

        result = self._dbCon.executeInsert(query, params)
        return result
        

        # query2 = """
        #     DECLARE	
        #     @OutRegID nvarchar(60)

        #     EXEC	 [st].[RegistorVisitor]
        #     @FirstName = ?,
        #     @LastName = ?,
        #     @GraduationClass = ?,
        #     @Gender = ?,
        #     @Programs = ?,
        #     @OutRegID = @OutRegID OUTPUT

        #     SELECT	@OutRegID as N'@OutRegID'
        #                         """    
        # params =  (self.name, self.lname , self.graduationClass, self.gender, self.programs)
        # result = self._dbCon.executeInsert(query2, params)
       
        
        # return result

    
        