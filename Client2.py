from google.cloud import storage
import requests
import json
import time

# Configura il nome del bucket e del file
BUCKET_NAME = 'bucket-delivery'
FILE_NAME = 'delivery.csv'

# Funzione per scaricare il file CSV dal bucket
def download_csv_from_bucket(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    return content

# Funzione principale che viene chiamata quando viene attivata la Cloud Function
def client(request):
    # URL del server (modifica questo URL con il tuo server effettivo)
    base_url = 'http://127.0.0.1:8080/raccolta_dati'

    # Scarica il CSV dal bucket
    csv_content = download_csv_from_bucket(BUCKET_NAME, FILE_NAME)

    # Leggi il contenuto del CSV
    lines = csv_content.splitlines()

    # Processa ogni riga del CSV (salta l'intestazione)
    for line in lines[1:]:
        ID, Delivery_person_ID, Delivery_person_Age, Delivery_person_Ratings, Restaurant_latitude, Restaurant_longitude, Delivery_location_latitude, Delivery_location_longitude, Type_of_order, Type_of_vehicle, Time_taken_min = line.strip().split(',')

        # Crea i dati per l'invio
        delivery_data = {
            'ID': ID,
            'Delivery_person_ID': Delivery_person_ID,
            'Delivery_person_Age': Delivery_person_Age,
            'Delivery_person_Ratings': Delivery_person_Ratings,
            'Restaurant_location': [Restaurant_latitude, Restaurant_longitude],
            'Delivery_location': [Delivery_location_latitude, Delivery_location_longitude],
            'Type_of_order': Type_of_order,
            'Type_of_vehicle': Type_of_vehicle,
            'Time_taken_min': Time_taken_min
        }

        # Invia i dati al server
        response = requests.post(base_url, json={'Dati': json.dumps(delivery_data)})
        time.sleep(1)  # Pausa di un secondo tra le richieste

        if response.status_code == 200:
            print(f"Dati inviati con successo per ID {delivery_data['ID']}")
        else:
            print(f"Errore nell'invio dei dati per l'ID {delivery_data['ID']} - Error: {response.text}")

    return 'done'  # La funzione deve restituire un messaggio quando completata
