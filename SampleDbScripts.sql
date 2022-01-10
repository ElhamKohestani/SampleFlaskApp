
CREATE DATABASE SampleDb;
print('database SampleDb created');
GO


USE SampleDb;
GO

CREATE SCHEMA st;
GO

CREATE SCHEMA look;
Go
print('Sample schema st and look created st stands for student');





CREATE TABLE look.[SequenceController](
	[Name] [varchar](50) NOT NULL,
	[Prefix] [varchar](10) NOT NULL,
	[LastValue] [varchar](50) NULL,
	[LastYear] [smallint] NOT NULL,
	[LastNumber] [int] NULL
	);
ALTER TABLE look.[SequenceController] ADD CONSTRAINT pk_look_SequenceController_Name_Lyear PRIMARY KEY ([Name], LastYear);

print('table sequence controller to control the sequence for studentID created');
GO



CREATE TABLE look.Program
(
	ID SMALLINT NOT NULL,
	Abbreviation VARCHAR(10) NOT NULL,
	Identifier VARCHAR(200) NOT NULL
);

INSERT INTO look.Program (ID, Abbreviation, Identifier)
VALUES (1, 'BCS', 'Bachelor of Computer Science'),
(2, 'BBA', 'Bachelor of Business Administration');


print('table programs with initial seeding of two records created');
GO

CREATE TABLE st.Visitor
(
	ID VARCHAR(20) NOT NULL,
	[Name] VARCHAR(200) NOT NULL,
	LastName VARCHAR(200) NOT NULL,
	Gender VARCHAR(10) NOT NULL,
	GraduationClass SMALLINT NOT NULL,
	RegistrationDate DATETIME2
);
ALTER TABLE st.Visitor ADD CONSTRAINT pk_st_visitor_id PRIMARY KEY (ID);
ALTER TABLE st.Visitor ADD CONSTRAINT df_st_visitor_date DEFAULT GETDATE() FOR RegistrationDate;

print('table visitor created for visiting students');
GO

CREATE TABLE st.VisitorProgram
(
	VisitorID VARCHAR(20) NOT NULL,
	ProgramID SMALLINT NOT NULL
);

ALTER TABLE st.VisitorProgram ADD CONSTRAINT pk_st_visitor_program PRIMARY KEY (VisitorID, ProgramID);
ALTER TABLE st.VisitorProgram ADD CONSTRAINT fk_st_visitor_ID FOREIGN KEY (VisitorID) REFERENCES st.Visitor(ID) ON DELETE CASCADE ; 

print('table visitor programs for storing student desired program of study. It can be one or many');
Go

CREATE PROC [look].[GetRegID] (@GeneratedID VARCHAR(50) OUTPUT)
AS
BEGIN
	
    DECLARE @CustomSequenceName VARCHAR(50) = 'RegistrationSequence'
	DECLARE @Prefix VARCHAR(10) = 'RG'
    DECLARE @Year               SMALLINT = YEAR(GETDATE())
    DECLARE @LenOfNumber        TINYINT = 5
    DECLARE @GeneratedValue     VARCHAR(50)


SET XACT_ABORT ON
BEGIN TRAN
    IF NOT EXISTS(SELECT * FROM look.SequenceController s WITH(HOLDLOCK) WHERE s.Name = @CustomSequenceName AND s.LastYear = @Year)
    BEGIN
        INSERT  look.[SequenceController]([Name], Prefix, LastValue, LastYear, LastNumber) 
        VALUES  (@CustomSequenceName, @Prefix, NULL, @Year, 1)
    END
    UPDATE  s
    SET     LastNumber      = IIF(LastValue IS NULL, LastNumber, LastNumber + 1) + IIF(LastNumber = REPLICATE('9', @LenOfNumber), 1/0, 0),
            @GeneratedValue = LastValue = Prefix + LTRIM(@Year) + '-' + RIGHT(REPLICATE('0', @LenOfNumber)  + LTRIM(IIF(LastValue IS NULL, LastNumber, LastNumber + 1)), @LenOfNumber)
    FROM    look.SequenceController s WITH(HOLDLOCK)
    WHERE   s.Name = @CustomSequenceName
    AND     s.LastYear = @Year

	SELECT @GeneratedID = @GeneratedValue
COMMIT

END
print('Stored procedure to control sequence generation created');
GO

-- stored procedure creation for the registration procedure



CREATE PROC [st].[RegistorVisitor]
(

@FirstName VARCHAR(200),
@LastName VARCHAR(200),
@GraduationClass SMALLINT= NULL,
@Gender VARCHAR(10),
@Programs AS VARCHAR(200), -- I could use a table type but the Pyodbc has some issues with Table Valued Parameters
@OutRegID NVARCHAR(60) OUTPUT
)
AS
BEGIN

BEGIN TRY
	BEGIN TRAN
		DECLARE @GeneratedID VARCHAR(50)
		DECLARE @RegID VARCHAR(50)
		EXEC look.GetRegID @GeneratedID out
		
		SELECT @RegID =@GeneratedID



		-- OPERATION 1
		INSERT INTO [st].[Visitor]
				   ([ID]
				   ,[Name]
				   ,[LastName]
				   ,[Gender]
				   ,[GraduationClass]
				   )
			 VALUES
				   (@RegID
				   ,@FirstName
				   ,@LastName
				   ,@Gender
				   ,@GraduationClass);
           



		-- OPERATION 2
		DECLARE @ProgramID_Splitter VARCHAR(1) = '|';
		
		
		DECLARE @ProgramID SMALLINT;

		WHILE (CHARINDEX(@ProgramID_Splitter, @Programs) > 0)
		BEGIN

			SET @ProgramID = CONVERT(SMALLINT, SUBSTRING(@Programs, 0, CHARINDEX(@ProgramID_Splitter, @Programs)));
			SET @Programs = SUBSTRING(@Programs, CHARINDEX(@ProgramID_Splitter, @Programs) + 1, LEN(@Programs));

			INSERT INTO st.VisitorProgram(VisitorID, ProgramID)
			VALUES (@RegID, @ProgramID);

		END


		SELECT @OutRegID = @RegID
	COMMIT
END TRY
BEGIN CATCH
	ROLLBACK TRAN
END CATCH

END;

print('Stored procedure for registering students created');
GO


CREATE PROC [st].[UpdateVisitor]
(
@RegID NVARCHAR(60),
@FirstName VARCHAR(200),
@LastName VARCHAR(200),
@GraduationClass SMALLINT,
@Gender VARCHAR(10),
@Programs AS VARCHAR(200)
)
AS
BEGIN

BEGIN TRY
	BEGIN TRAN
		


		-- OPERATION 1


		UPDATE [st].[Visitor]
		   SET 
			  [Name] = @FirstName
			  ,[LastName] = @LastName
			  ,[Gender] = @Gender
			  ,[GraduationClass] = @GraduationClass
			  ,[RegistrationDate] = GETDATE()
		 WHERE ID = @RegID






		-- OPERATION 2

		DELETE FROM st.VisitorProgram WHERE VisitorID = @RegID;
		DECLARE @ProgramID_Splitter VARCHAR(1) = '|';

		
		DECLARE @ProgramID SMALLINT;

		WHILE (CHARINDEX(@ProgramID_Splitter, @Programs) > 0)
		BEGIN

			SET @ProgramID = CONVERT(SMALLINT, SUBSTRING(@Programs, 0, CHARINDEX(@ProgramID_Splitter, @Programs)));
			SET @Programs = SUBSTRING(@Programs, CHARINDEX(@ProgramID_Splitter, @Programs) + 1, LEN(@Programs));

			INSERT INTO st.VisitorProgram(VisitorID, ProgramID)
			VALUES (@RegID, @ProgramID);

		END

	COMMIT
END TRY
BEGIN CATCH
	ROLLBACK TRAN
END CATCH

END;
print('Stored procedure for update of visitor and its programs created');

GO
