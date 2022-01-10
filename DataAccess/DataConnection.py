

from typing import final
import pyodbc


class DbConnection:

    def __init__(self):    
        self._server = 'localhost\MSS12' 
        self._database = 'SampleDb' 
        self._username = 'sa' 
        self._password = '' 
        self._cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._server+';DATABASE='+self._database+';UID='+self._username+';PWD='+ self._password, autocommit= False)
        self._cursor = self._cnxn.cursor()
    
    def __NoNoneElements__(self, parameters: tuple):
        for element in parameters:
            if element == None:
                return False
        return True
    
    def __buildResultSet__(self, cursorRows, cursorDescription):
        columns = [column[0] for column in cursorDescription]

        resultSet = []
        for row in cursorRows:
            resultSet.append(dict(zip(columns, row)))
        
        return resultSet



    def executeSelect(self, query, paramters: tuple = ()):
        raw_data = None
        try:
            
            if (len(paramters) > 0 and self.__NoNoneElements__(paramters)):
                raw_data = self._cursor.execute(query, paramters).fetchall()
            else:
                raw_data = self._cursor.execute(query).fetchall()

            self._cursor.commit()
            return raw_data
            #return self.__buildResultSet__(raw_data, self._cursor.description)

        except pyodbc.DatabaseError as err:
            self._cursor.rollback()
            print('select error ', err)
        
       

    def executeInsert(self, query, paramters: tuple = ()):
        result_set = None
        try:
            
            result_set = self._cursor.execute(query, paramters)
            self._cursor.commit()
            return result_set

        except pyodbc.DatabaseError as err:
            self._cursor.rollback()
            print('insert error ', err)
        finally:
            self._cnxn.close()
    
    def executeDelete(self, query, paramters: tuple = ()):
        rowsAffected = None
        try:
            
            rowsAffected = self._cursor.execute(query, paramters)
            self._cursor.commit()
            return rowsAffected

        except pyodbc.DatabaseError as err:
            self._cursor.rollback()
            print('delete error ', err)
        finally:
            self._cnxn.close()
    


       






    