from pocketbase import PocketBase
from pocketbase.client import FileUpload
from time import sleep
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def callback(e):
    if e:
        logging.info(f"Record: {e.record}")
        try:
            # Access the 'letter' attribute if it exists
            logging.info(f"Letter: {e.record.letter}")
        except KeyError:
            logging.error("Field 'letter' not found in the record.")

if __name__ == '__main__':
    client = PocketBase('https://pockets.db.fixthecode.xyz')

    # Authenticate as admin
    try:
        admin_data = client.admins.auth_with_password("fred+live@mildlyupset.com", "dZT$wMX9rQ73~,=")
    except Exception as ex:
        logging.error(f"Authentication failed: {ex}")
        exit(1)

    # Subscribe to the collection and bind the callback
    result = client.collection("dear_ai").subscribe(callback)

    try:
        while True:
            sleep(3)
    except KeyboardInterrupt:
        logging.info("Graceful shutdown upon user request")
    except Exception as ex:
        logging.error(f"An error occurred: {ex}")