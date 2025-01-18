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
dbName = 'delivery-437306'
coll = 'consegne'
db = firestore.Client.from_service_account_json('C:\\Users\\Pietro\\OneDrive\\Desktop\\Progetto Elisa\\HTML Progetto Delivery\\credentials.json', database=dbName)

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

@app.route('/prova', methods=['POST','GET']) #leggiamo i dati per passarli al grph.html
def prova():
    db = {}
    data = request.values['Data']
    print(data)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 , debug=True)
    
print('ciao 3')