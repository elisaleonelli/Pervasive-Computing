import requests 
from requests import get, post
import time
import json 
base_url = 'http://127.0.0.1:5000'
with open('C:\\Users\\Pietro\\OneDrive\\Desktop\\Progetto Elisa\\HTML Progetto Delivery\\delivery.csv') as f:
    for l in f.readlines()[1:]:
        ID, Delivery_person_ID, Delivery_person_Age, Delivery_person_Ratings, Restaurant_latitude, Restaurant_longitude, Delivery_location_latitude, Delivery_location_longitude, Type_of_order, Type_of_vehicle, Time_taken_min = l.strip().split(',')
        
        # Chiave unica per la posizione del ristorante e della consegna
        restaurant_location = [Restaurant_latitude,Restaurant_longitude]
        delivery_location = [Delivery_location_latitude,Delivery_location_longitude]

        delivery_data = {
            'ID': ID,
            'Delivery_person_ID': Delivery_person_ID,
            'Delivery_person_Age': Delivery_person_Age,
            'Delivery_person_Ratings': Delivery_person_Ratings,
            'Restaurant_location': restaurant_location,
            'Delivery_location': delivery_location,
            'Type_of_order': Type_of_order,
            'Type_of_vehicle': Type_of_vehicle,
            'Time_taken_min': Time_taken_min
        }
        r = requests.post(base_url, {'Data': json.dumps(delivery_data)})
        time.sleep(1) #pausa di un secondo tra le richieste per evitare sovraccaricamento server 
        if r.status_code == 200:
            print(f"Successfully sent data for ID {delivery_data['ID']}")
        else:
            print(f"Failed to send data for ID {delivery_data['ID']} - Error: {r.text}")

        
print('done')

'''import requests 
from requests import get, post
import time
import json

print('via')

# URL del server
server_url = 'http...'

with open('C:\\Users\\Pietro\\OneDrive\\Desktop\\Progetto Elisa\\HTML Progetto Delivery\\delivery.csv') as file:
    for line in file.readlines()[1:]:
        ID, Delivery_person_ID, Delivery_person_Age, Delivery_person_Ratings, Restaurant_latitude, Restaurant_longitude, Delivery_location_latitude, Delivery_location_longitude, Type_of_order, Type_of_vehicle, Time_taken_min = line.strip().split(',')
        
        # Chiave unica per la posizione del ristorante e della consegna
        restaurant_location = [Restaurant_latitude,Restaurant_longitude]
        delivery_location = [Delivery_location_latitude,Delivery_location_longitude]

        delivery_data = {
            'ID': ID,
            'Delivery_person_ID': Delivery_person_ID,
            'Delivery_person_Age': Delivery_person_Age,
            'Delivery_person_Ratings': Delivery_person_Ratings,
            'Restaurant_location': restaurant_location,
            'Delivery_location': delivery_location,
            'Type_of_order': Type_of_order,
            'Type_of_vehicle': Type_of_vehicle,
            'Time_taken_min': Time_taken_min
        }

        response = requests.post(server_url, json={'Dati': json.dumps(delivery_data)})  # Formato JSON corretto
        time.sleep(1)  # Pausa di un secondo tra le richieste

        if response.status_code == 200:
            print(f"Dati inviati con successo per ID {delivery_data['ID']}")
        else:
            print(f"Errore nell'invio dei dati per l'ID {delivery_data['ID']} - Error: {response.text}")

print('done')


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

# URL del server
base_url = 'http...'

# Scarica il CSV dal bucket
csv_content = download_csv_from_bucket(BUCKET_NAME, FILE_NAME)

# Leggi il contenuto del CSV
lines = csv_content.splitlines()

# Processa ogni riga del CSV (salta l'intestazione)
for line in lines[1:]:
    ID, Delivery_person_ID, Delivery_person_Age, Delivery_person_Ratings, Restaurant_latitude, Restaurant_longitude, Delivery_location_latitude, Delivery_location_longitude, Type_of_order, Type_of_vehicle, Time_taken_min = line.strip().split(',')
    
    # Chiave unica per la posizione del ristorante e della consegna
    restaurant_location = [Restaurant_latitude, Restaurant_longitude]
    delivery_location = [Delivery_location_latitude, Delivery_location_longitude]

    # Crea i dati per l'invio
    delivery_data = {
        'ID': ID,
        'Delivery_person_ID': Delivery_person_ID,
        'Delivery_person_Age': Delivery_person_Age,
        'Delivery_person_Ratings': Delivery_person_Ratings,
        'Restaurant_location': restaurant_location,
        'Delivery_location': delivery_location,
        'Type_of_order': Type_of_order,
        'Type_of_vehicle': Type_of_vehicle,
        'Time_taken_min': Time_taken_min
    }

    # Invia i dati al server
    response = requests.post(base_url , json={'Dati': json.dumps(delivery_data)})  # Formato JSON corretto
    time.sleep(1)  # Pausa di un secondo tra le richieste

    if response.status_code == 200:
        print(f"Dati inviati con successo per ID {delivery_data['ID']}")
    else:
        print(f"Errore nell'invio dei dati per l'ID {delivery_data['ID']} - Error: {response.text}")

print('done')'''

