from flask import Flask, url_for, request
from flask.templating import render_template
from werkzeug.utils import redirect
from DataAccess.ProgramDA import Program
from DataAccess.RegistrationDA import Visitor

app = Flask(__name__, template_folder= "pages")

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/registration/deleteVisitor/<id>", methods=['GET'])
def deleteVisitor(id):
    visitor = Visitor()
    rowsAffected = visitor.DeleteVisitor(id)
    return redirect("/registration")

@app.route("/registration/updateVisitor/<id>", methods= ['GET'])
def updateVisitor(id):
    program = Program()
    programs = program.getProgram()

    visitor = Visitor()
    visitor_data = visitor.getVisitor(id)
    visitor_programs = visitor.getVisitorPrograms(id)
    

    return render_template("registration.html", programs  = programs, visitor_programs = visitor_programs, visitor_data = visitor_data)

@app.route('/registration', methods=['POST', 'GET'])
def registration():

    program = Program()
    programs = program.getProgram()

    visitor = Visitor()
    tenRecentlyRegistered = visitor.getRegistered(10)
    

    if(request.method == 'POST'):
        v_registrationId = request.form["regID"]
        v_name = request.form["name"]
        v_lName = request.form["lName"]
        v_gender = request.form["gender"]
        v_selected_programs = request.form.getlist("programs")
        v_graduationClass = request.form["graduationClass"]

        # Not implmented the client side validation so the list may be empty. In order to avoid error 1 will be passed as program id in case of empty list.
        # programs_text = "1" if len(v_selected_programs) < 1 else v_selected_programs[0]
        programs_text = ""

        for p in v_selected_programs:
            programs_text += (p + "|") 


        try:
            
            visitor = Visitor(registrationId= v_registrationId, name= v_name, lname= v_lName, graduationClass= int(v_graduationClass), gender= v_gender, programs= programs_text )
            res = visitor.registerVisitor()
            return redirect("/registration")
            
        except:
            # or a custom logging feature could be implemented here
            print('exception occurred')
    else:
        return render_template('registration.html', programs = programs, registries = tenRecentlyRegistered)
        



        

    


@app.route('/programs')
def getProgram():
    program = Program()
    programs = program.getProgram()

    return render_template('programs.html', programs = programs)




if(__name__ == '__main__'):
    app.run(debug= True)
