from pocketbase import PocketBase
from pocketbase.client import FileUpload
from time import sleep
import logging
from datetime import datetime
# Setup logging
logging.basicConfig(level=logging.INFO)

client = PocketBase('https://pockets.db.fixthecode.xyz')

# Authenticate as admin
try:
    admin_data = client.admins.auth_with_password("fred+live@mildlyupset.com", "dZT$wMX9rQ73~,=")
except Exception as ex:
    logging.error(f"Authentication failed: {ex}")
    exit(1)

def checkDatabase():
    today = datetime.today().strftime('%Y-%m-%d')
    result = client.collection("dear_ai_live").get_list(
    1, 20, { "filter": f'status = "toPrint" && created > "{today} 00:00:00"',"sort": 'created'})
    if len(result.items) > 0:
        print(result.items[0].id)
        item = result.items[0]
        logging.info(f" Found a new letter")
    else:
        item = False
        logging.info(f" No items to print")
    return item

    
def updateItem(id, status):
    
    result = client.collection("dear_ai_live").update(id
    ,{
        "status": f"{status}",
    })
    
    



            
            
def initWriting(item):
    id = item.id
    logging.info(f"{item.subject}")
    sleep(10)
    updateItem(id, 'printed')
    

if __name__ == '__main__':

    # # Subscribe to the collection and bind the callback
    # result = client.collection("dear_ai").subscribe(callback)

    try:
        while True:
            sleep(5)
            item = checkDatabase()
            if item:
                initWriting(item)

    except KeyboardInterrupt:
        logging.info("Graceful shutdown upon user request")
    except Exception as ex:
        logging.error(f"An error occurred: {ex}")