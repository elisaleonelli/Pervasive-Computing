from flask import Flask, request, redirect, url_for, render_template
from requests import get, post
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from google.cloud import firestore
import json
from joblib import load
from google.cloud import storage
from google.cloud import pubsub_v1
from google.auth import jwt

class User(UserMixin):
    def __init__(self, email):
        super().__init__()
        self.id = email  # Imposta l'email come identificatore univoco
        self.email = email  # Salva l'email come attributo 

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)
login.login_view = 'login'  # Reindirizza a Flask per la pagina di login, non a una statica

# apertura connessione DB Firestore
dbName = 'progetto'
coll = 'consegne'
db = firestore.Client.from_service_account_json("credentials.json", database=dbName)

credenziali = {"elisaleonelli2000@gmail.com" : "Micetto",
          "266983@studenti.unimore.it" : "Unimore"}

# questa parte di codice mi riporta alla pagina iniziale quando apro il server 
@app.route('/')
def main():
    return redirect(url_for('static', filename='paginainiziale.html'))

print('ciao1')

@login.user_loader
def load_user(email):
    if email in credenziali:
        return User(email)
    return None

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email in credenziali and password == credenziali[email]:
        return redirect(url_for('static', filename='home.html'))
    return redirect(url_for('static', filename='login.html'))


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('main'))  # Reindirizza alla home dopo il logout

print('ciao2')


def upload_data(data):
    print("Salvataggio dati")
    docID = data['ID']  # ID del documento
    docVal = {
        'Delivery_person_ID': data['Delivery_person_ID'],
        'Delivery_person_Age': data['Delivery_person_Age'],
        'Delivery_person_Ratings': data['Delivery_person_Ratings'],
        'Restaurant_location': data['Restaurant_location'],
        'Delivery_location': data['Delivery_location'],
        'Type_of_order': data['Type_of_order'],
        'Type_of_vehicle': data['Type_of_vehicle'],
        'Time_taken_min': data['Time_taken_min']
    }
    print("docVal: ", docVal)

    docRef = db.collection(coll).document(docID)  # Riferimento al documento
    docRef.set(docVal)  # Scrittura su Firestore

    # Endpoint per ricevere dati dal client
@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        print("Dati ricevuti:", data)
        upload_data(data)
        return "Dati salvati con successo", 200
    except Exception as e:
        print(f"Errore: {e}")
        return f"Errore: {e}", 500

    
# Endpoint per recuperare i dati da Firestore
@app.route('/upload/<docID>', methods=['GET'])
def get_data(docID):
    # Riferimento al documento
    docRef = db.collection(coll).document(docID)
    doc = docRef.get()  # Recupera il documento

    if doc.exists:
        # Converte il documento in un dizionario e lo restituisce
        return doc.to_dict(), 200
    else:
        return {"error": "Documento non trovato"}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)
    
print('ciao 3')
