from flask import Flask, render_template
from flask_mysqldb import MySQL
import os
#create a Flask application instance
app = Flask(__name__)
# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sesamm'
#configure the type of cursor to be used when interacting with  MySQL database  as DictCursor  
#  It returns the rows of a query as dictionaries instead of tuples
# allowing the results to be accessed using keys (column names) instead of indexes.
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Initialize the app for use with this MySQL class
mysql.init_app(app)
# Function to retrieve the number of rows in the "test_file" table where at least one contains the value 0.
def get_number_warnings():
    # Create a cursor object to execute database commands
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT *FROM test_file WHERE 0 IN (Date,sentiment_positive,sentiment_negative,emotion_joy,emotion_fear,volume);")
    return num_rows
# Function to retrieve number of  rows from the "test_file" table.
def get_all_observations():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM test_file")
    return num_rows

# Route for the main page of the application
@app.route('/')
def admin():
    curso = mysql.connection.cursor()
    all_observations = curso.execute("SELECT * FROM test_file")
    result = curso.fetchall()
    metric=2
    warning=get_number_warnings()
    # return the "pages/index.html" template and pass in the query result, the number of observations
    #  the metric value, and the number of warnings as variables
    return render_template('pages/index.html', result=result, row=all_observations, metrics=metric,
                           nb_warning=warning)

# Route for the page that displays the warnings
@app.route('/warnings')
def get_warnings():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT *FROM test_file WHERE 0 IN (Date,sentiment_positive,sentiment_negative,emotion_joy,emotion_fear,volume);")
    result = curso.fetchall()
    #retrieve the total number of observations
    all_observations=get_all_observations()
    metric=2
    # return the "pages/warnings.html" template and pass in the query result, 
    # the number of warnings, the metric value, and the total number of observations as variables
    return render_template('pages/warnings.html', result=result, nb_warning=num_rows, metrics=metric,
                           observations=all_observations) 

# Route for the page that displays some visualisations
@app.route('/visualisation')
def orders():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM test_file")
    result = curso.fetchall()
    #retrieve the values of Date
    labels_d = []
    #retrieve the values sentiment positive 
    label_sp = []
    #retrieve the sentiment negative 
    label_sn = []
    #retrieve the values of emotion of joy
    label_ej=[]
    #retrieve the values of emotion of fear 
    label_ef=[]
    #retrieve the values of volume 
    label_v=[]
    #retrieve the values of values column 
    missing_values=[]
    #retrieve the values of the missing dates
    labels_missing=[]
    #Loops through each row in the results of the query  and appends the values of each column
    for row in result:
                labels_d.append(row["Date"])
                label_sp.append(row["sentiment_positive"])
                label_sn.append(row["sentiment_negative"])
                label_ej.append(row["emotion_joy"])
                label_ef.append(row["emotion_fear"])
                label_v.append(row["volume"])
    #retrieve missing date of January 
    curso = mysql.connection.cursor()
    num_rows_missing = curso.execute("SELECT * FROM test_file LIMIT 26")
    result = curso.fetchall()
    for row in result:
                missing_values.append(row["sentiment_positive"])
                labels_missing.append(row["Date"])
    #append the missing dates 
    labels_missing.insert(4,'2020-01-05')
    missing_values.insert(4,'NaN')
    missing_values.insert(23,'NaN')
    labels_missing.insert(23,'2020-01-24')
    missing_values.insert(24,'NaN')
    labels_missing.insert(24,'2020-01-25')
    missing_values.insert(25,'NaN')
    labels_missing.insert(25,'2020-01-26')
    missing_values.insert(26,'NaN')
    labels_missing.insert(26,'2020-01-27')
    warning=get_number_warnings()
    metric=2
    all_observations=get_all_observations()

    return render_template('pages/metrics.html',labels_missing=labels_missing,missing_values=missing_values,label_v=label_v,label_ej=label_ej,label_ef=label_ef,label_sn=label_sn, label_sp=label_sp,labels_d=labels_d,nb_warning=warning, metrics=metric,
                           observations=all_observations) 


if __name__ == '__main__':
    app.run(debug=True)
