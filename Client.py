import requests 
from requests import get, post
import time
import json 
#base_url = 'http://127.0.0.1:5000'
base_url = 'https://progettopervasivecomputing.nw.r.appspot.com/'
with open('delivery.csv') as f:
    for l in f.readlines()[1:6]:
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
        #time.sleep(1) #pausa di un secondo tra le richieste per evitare sovraccaricamento server 
        r = requests.post(base_url + '/prova', json={'Data': json.dumps(delivery_data)})
        if r.status_code == 200:
            print(f"Successfully sent data for ID {delivery_data['ID']}")
        else:
            print(f"Failed to send data for ID {delivery_data['ID']} - Error: {r.text}")

        
print('done')


