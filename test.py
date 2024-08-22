import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
cred = credentials.Certificate(r'C:\Users\PMLS\Downloads\kotlin-3cc89-61acf6acefa0.json') 
firebase_admin.initialize_app(cred)
db = firestore.client()

font = cv2.FONT_HERSHEY_PLAIN

url = 'http://10.10.4.73/'  # esp-cam
esp32_wroom_ip = '10.10.4.90'  #  ESP32-WROOM-32

cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

prev = ""
pres = ""

def check_order_fulfilled(order_id):
    try:
        doc_ref = db.collection('Orders').document(order_id)
        doc = doc_ref.get()
        if doc.exists:
            fulfilled = doc.to_dict().get('fulfilled', True)
            if not fulfilled:
                # Update the fulfilled field to true
                doc_ref.update({'fulfilled': True})
                return True
            else:
                return False
        else:
            print(f"No such document with OrderId: {order_id}")
            return False
    except Exception as e:
        print(f"Error checking Firestore document: {e}")
        return False

def update_quantity(machine_id, item_id, quantity_to_subtract):
    try:
        doc_ref = db.collection('Machines').document(machine_id).collection('items').document(item_id)
        doc = doc_ref.get()
        if doc.exists:
            current_quantity = int(doc.to_dict().get('quantity', '0'))
            new_quantity = max(current_quantity - quantity_to_subtract, 0)
            doc_ref.update({'quantity': str(new_quantity)})
            print(f"Updated {item_id}: new quantity is {new_quantity}")
        else:
            print(f"No such sub-document with ItemId: {item_id}")
    except Exception as e:
        print(f"Error updating Firestore document: {e}")

while True:
    img_resp = urllib.request.urlopen(url + 'cam-hi.jpg')
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)

    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        pres = obj.data
        if prev == pres:
            pass
        else:
            print("Type:", obj.type)
            print("Data: ", obj.data)
            
            data_str = obj.data.decode()
            if "Machine ID: 1708808943016" in data_str:
                # Find the data after "Order ID:"
                order_id_index = data_str.find("Order ID:")
                items_index = data_str.find("Items:")
                if order_id_index != -1 and items_index != -1:
                    order_id = data_str[order_id_index + len("Order ID:"):items_index].strip()#remove white spaces
                    items_data = data_str[items_index + len("Items:"):].strip()

                    if check_order_fulfilled(order_id):
                        items = items_data.split('\n')
                        for item in items:
                            if ':' in item:
                                item_id, quantity_str = item.split(':')
                                item_id = item_id.strip()
                                quantity = int(quantity_str.strip())
                                update_quantity('1708808943016', item_id, quantity)
                        
                        # Send decoded data to ESP32-WROOM-32
                        requests.post(f'http://{esp32_wroom_ip}/data', data=items_data, timeout=5)
                        prev = pres
                    else:
                        print("Order has already been fulfilled. Data not transmitted.")
                else:
                    print("OrderId or Items data not found.")
            else:
                print("Invalid Machine ID. Data not transmitted.")
                
        cv2.putText(frame, str(obj.data), (50, 50), font, 2, (255, 0, 0), 3)

    cv2.imshow("live transmission", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
