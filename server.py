from flask import Flask, render_template, request, redirect, session, flash
# import the function that will return an instance of a connection 
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "Secret"
@app.route('/')
def index():
    mysql = connectToMySQL('dojo_survey')
    #call the query_db function, pass in the query as a string
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template('survey.html', all_users = users)

@app.route('/submitted_survey', methods =['POST'])
def submit():
    is_valid = True # assume True
    if len(request.form['name']) < 1:
        is_valid = False
        # display validation error
        flash('Please enter a first name')

    if len(request.form['location']) < 1:
        is_valid = False
        # display validation error
        flash('Please select a location')

    if len(request.form['language']) < 2:
        is_valid = False
        # display validation error
        flash ('Please select a language')

    if not is_valid:    # if any of the fields switched our is_valid toggle to False
        return redirect('/')    # redirect back to the method that displays the index page
    
    else: # if is_valid is still True, all validation checks were passed 
        mysql = connectToMySQL('dojo_survey')
        query ="INSERT INTO users (name, location, language, comment) VALUES (%(name)s, %(loc)s, %(lang)s, %(comm)s);"
        data = {
            'name': request.form['name'],
            'loc':request.form['location'],
            'lang' : request.form['language'],
            'comm' : request.form['comment']
        }
        user_id = mysql.query_db(query, data)
        print(user_id)
        # add user to database
        # display success message
        # redirect to a method that displays a success pagee
    return redirect("/show_submitted")

@app.route('/show_submitted')
def show_submitted():
    mysql = connectToMySQL('dojo_survey')
    query = "SELECT * FROM users"
    user_id = mysql.query_db(query)
    return render_template ('submitted_survey.html', users = user_id)

if __name__ == "__main__":
    app.run(debug=True)