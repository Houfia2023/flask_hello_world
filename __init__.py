from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
app = Flask(__name__)                                                                                                                  
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/fr/")
def monfr():
    return "<h2>Bonjour tout le monde !</h2>"

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
    
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)
    
@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/search/<nom_search>')
def Search(nom_search):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE nom LIKE ?;", ('%' + nom_search +'%',))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)
    
@app.route('/ajouter_client/', methods=['GET', 'POST'])
def nouveau():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']
        # Traiter les données (par exemple, les afficher dans la console)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        #cursor.execute('SELECT * FROM clients;')
        cursor.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?);", (nom, prenom, adresse))
        conn.commit()
        conn.close()
        #print(f"Nom: {nom}")
        #print(f"prenom: {prenom}")
        #print(f"adresse: {adresse}")
        return render_template('confirmation.html')
    return render_template('formulaire.html')
    
    
if __name__ == "__main__":
  app.run(debug=True)
