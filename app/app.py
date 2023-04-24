from flask import Flask, render_template, request, redirect,url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#   CONEXION MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskusers'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

# Decorador
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    return render_template('index.html', users = data)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']
        country = request.form['country']
        postalcode = request.form['postalcode']
        labexp = request.form['labexp']
        training = request.form['training']
        language = request.form['language']
        skills = request.form['skills']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (email, name, lastname, country, postalcode, labexp, training, language, skills) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (email, name, lastname, country, postalcode, labexp, training, language, skills))
        mysql.connection.commit()
        flash('User added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit_user(id) :
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-user.html', user = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']
        country = request.form['country']
        postalcode = request.form['postalcode']
        labexp = request.form['labexp']
        training = request.form['training']
        language = request.form['language']
        skills = request.form['skills']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET email = %s, 
                name = %s, 
                lastname = %s, 
                country = %s, 
                postalcode = %s, 
                labexp = %s, 
                training = %s, 
                language = %s, 
                skills = %s
            WHERE id = %s
        """, (email, name, lastname, country, postalcode, labexp, training, language, skills, id))
        mysql.connection.commit()
        flash('User updated successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_user(id) :
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed succesfully')
    return redirect(url_for('Index'))

if __name__=='__main__':
    app.run(debug=True, port=5000)