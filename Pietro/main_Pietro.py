from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask import Flask,request,redirect,url_for,render_template
from requests import get, post
import json
from google.cloud import firestore

app = Flask(__name__)

usersdb = {
'elisaleonelli2000@gmail.com':'Micetto'
}

#vengo indirizzato alla pagina iniziale quando apro l'applicazione
@app.route('/')
def main():
    return redirect(url_for('static', filename='paginainiziale.html'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email in usersdb and password == usersdb[email]:
        return redirect(url_for('static', filename='home.html'))
    return redirect(url_for('static', filename='login.html'))

@app.route('/maps', methods=['POST', 'GET'])
def read_data():
    db = firestore.Client.from_service_account_json('credentials.json', database='provaleonelli')
    doc_ref = db.collection('Table1').document('Ordini')
    if doc_ref.get().exists:
        diz = doc_ref.get().to_dict()
        r=[]
        for i in range(1, len(diz)+1):
            r.append([i, diz[str(i)]])
    else:
        print('document not found', 404)
    return json.dumps(r),200

@app.route('/salvataggio', methods=['POST'])
def store():
    #estraggo l'ID dell'ordine dalla request
    delivery = json.loads(request.values['Data']) #estraggo dalla request il dizionario con i dati dell'ordine corrispondente all'iterazione corrente
    ID = delivery['ID']#estraggo l'ID dell'ordine dal dizionario
    val = {
        'Delivery_ID': delivery['Delivery_ID'],
        'Delivery_age': delivery['Delivery_age'],
        'Delivery_ratings': delivery['Delivery_ratings'],
        'Restaurant_location': delivery['Restaurant_location'],
        'Delivery_location': delivery['Delivery_location'],
        'Type_of_order': delivery['Type_of_order'],
        'Type_of_vehicle': delivery['Type_of_vehicle'],
        'Time_taken': delivery['Time_taken']
    } #estraggo i valori dal dizionario e li inserisco in un nuovo dizionario

    db = firestore.Client.from_service_account_json('credentials.json', database='provaleonelli')# Inizializzo il client Firestore
    doc_ref = db.collection('Table1').document('Ordini') #faccio riferimento al documento "Ordini"

    if doc_ref.get().exists:
        #se il doc. esiste aggiorno il firestore
        diz = doc_ref.get().to_dict() #creo un dizionario diz con la versione vechia dei dati presenti nel firestore
        diz[ID] = val #aggiungo al dizionario la nuova coppia data-valore (ID-ordine).
                        # ora diz contiene tutti i dati già inseriti più quello nuovo proveniente dall' iterazione corrente
        doc_ref.update(diz)#aggiorno il doc di firestore con diz
    else:
        #se il doc. non esiste lo creo e inserisco il primo valore
        doc_ref.set({ID : val})
    return f"Dati memorizzati con successo"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)