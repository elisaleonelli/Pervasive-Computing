from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask import Flask, request, redirect, url_for, render_template
import json
from google.cloud import firestore

app = Flask(__name__)

usersdb = {
    'elisaleonelli2000@gmail.com': 'Micetto'
}

# Inizializza un contatore globale
order_count = 0
statistics_batch_size = 5  # Calcola le statistiche ogni X ordini ricevuti

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
    db = firestore.Client.from_service_account_json('credentials.json', database='progettoleonelli')
    doc_ref = db.collection('Table1').document('Ordini')
    if doc_ref.get().exists:
        diz = doc_ref.get().to_dict()
        r=[]
        for i in range(1, len(diz)+1):
            r.append([i, diz[str(i)]])
    else:
        print('document not found', 404)
    return json.dumps(r), 200

@app.route('/salvataggio', methods=['POST'])
def store():
    global order_count  # Usa il contatore globale

    # Estrai l'ID dell'ordine dalla request
    delivery = json.loads(request.values['Data'])  # Estrai i dati dell'ordine
    ID = delivery['ID']  # Estrai l'ID dell'ordine

    val = {
        'Delivery_ID': delivery['Delivery_ID'],
        'Delivery_age': delivery['Delivery_age'],
        'Delivery_ratings': delivery['Delivery_ratings'],
        'Restaurant_location': delivery['Restaurant_location'],
        'Delivery_location': delivery['Delivery_location'],
        'Type_of_order': delivery['Type_of_order'],
        'Type_of_vehicle': delivery['Type_of_vehicle'],
        'Time_taken': delivery['Time_taken']
    }  # Crea un nuovo dizionario con i dati dell'ordine

    db = firestore.Client.from_service_account_json('credentials.json', database='progettoleonelli')
    doc_ref = db.collection('Table1').document('Ordini')  # Riferimento al documento "Ordini"

    if doc_ref.get().exists:
        # Se il documento esiste, aggiorno il Firestore
        diz = doc_ref.get().to_dict()  # Ottieni la versione attuale dei dati
        diz[ID] = val  # Aggiungi il nuovo ordine al dizionario
        doc_ref.update({ID: val}) # Aggiorna il documento
    else:
        # Se il documento non esiste, lo creo e inserisco il primo ordine
        doc_ref.set({ID: val})

    order_count += 1  # Incrementa il contatore degli ordini ricevuti

    # Calcolare le statistiche ogni X ordini ricevuti
    if order_count % statistics_batch_size == 0:
        calculate_delivery_time_statistics()

    return f"Dati memorizzati con successo"

# Funzione per calcolare le statistiche del tempo di consegna, valutazione media e numero di consegne
def calculate_delivery_time_statistics():
    db = firestore.Client.from_service_account_json('credentials.json', database='progettoleonelli')
    doc_ref = db.collection('Table1').document('Ordini')

    if doc_ref.get().exists:
        diz = doc_ref.get().to_dict()
        driver_stats = {}

        # Controlliamo il contenuto del dizionario per debug
        if not diz:
            print("Errore: dizionario vuoto o struttura non corretta")
            return

        for ordine in diz.values():
            driver_id = ordine.get('Delivery_ID')  # Usa .get() per evitare errori di chiave

            if driver_id is None:
                print(f"Errore: 'Delivery_ID' mancante in ordine: {ordine}")
                continue  # Salta l'ordine se manca l'ID del driver

            delivery_time = float(ordine.get('Time_taken', 0))  # Converte in float e imposta 0 se mancante
            delivery_rating = float(ordine.get('Delivery_ratings', 0))  # Converte in float e imposta 0 se mancante

            if driver_id not in driver_stats:
                driver_stats[driver_id] = {
                    'total_time': 0, 
                    'order_count': 0, 
                    'total_rating': 0
                }

            driver_stats[driver_id]['total_time'] += delivery_time
            driver_stats[driver_id]['order_count'] += 1
            driver_stats[driver_id]['total_rating'] += delivery_rating

        driver_avg_time = {}
        driver_avg_rating = {}
        driver_total_orders = {}

        for driver_id, stats in driver_stats.items():
            avg_time = stats['total_time'] / stats['order_count']
            avg_rating = stats['total_rating'] / stats['order_count']
            total_orders = stats['order_count']

            driver_avg_time[driver_id] = avg_time
            driver_avg_rating[driver_id] = avg_rating
            driver_total_orders[driver_id] = total_orders

        # Salvataggio delle statistiche nel Firestore
        save_statistics_to_firestore(driver_avg_time, driver_avg_rating, driver_total_orders)

# Funzione per salvare le statistiche nel database
def save_statistics_to_firestore(avg_time, avg_rating, total_orders):
    db = firestore.Client.from_service_account_json('credentials.json', database='progettoleonelli')
    stats_ref = db.collection('Driver_Statistics').document('Statistics')
    stats_ref.set({
    'timestamp': firestore.SERVER_TIMESTAMP,
    'average_times': avg_time,  # Salviamo il dizionario
    'average_ratings': avg_rating,
    'total_orders': total_orders
    })
    print("Salvataggio statistiche:", avg_time, avg_rating, total_orders)



@app.route('/graph', methods=['POST', 'GET'])
def graph1_data():
    db = firestore.Client.from_service_account_json('credentials.json', database='progettoleonelli')
    doc_ref = db.collection('Driver_Statistics').document('Statistics')
    
    if doc_ref.get().exists:
        stats = doc_ref.get().to_dict()

        avg_times = stats.get('average_times', {})
        avg_ratings = stats.get('average_ratings', {})
        total_orders = stats.get('total_orders', {})
        
        # Converti i dati per passare alla grafica
        chart_data = []
        for driver_id in avg_times.keys():
            chart_data.append([driver_id,  avg_times.get(driver_id, 0), avg_ratings.get(driver_id, 0), total_orders.get(driver_id, 0)])
    else:
        print('Document not found', 404)

    # Renderizza la pagina con i dati
    return render_template('statistiche.html', data=chart_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
