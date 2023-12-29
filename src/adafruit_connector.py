import time
from Adafruit_IO import Client, Data, Feed, RequestError
from env import adafruit_user, adafruit_key
import pandas as pd

items_structure = {
    'Timestamp': [],
    'Barcode': [],
    'Description': [],
    'Expiration Date': [],
    'Quantity': [],
    'Date added': [],
    'Date modified': []
}

def read_items(key):
    # create an instance of the REST client.
    aio = Client(adafruit_user, adafruit_key)

    # Access existing or create new FEED using the name/key passed as parameter
    try:
        # Open Adafruit Feed, retrieve its data (which is in JSON format), create DataFrame from the JSON
        feed = aio.feeds(key)
        feed_data = aio.receive(feed.key)
        items = pd.read_json(feed_data.value)
    except RequestError:
        # If an error is thrown, we assume the Adafruit Feed does not exist
        # In this case we create a new Adafruit Feed, a new DataFrame using the predefined Structure, and store the new DataFrame in Adafruit
        feed = aio.create_feed(Feed(name=key, key=key, history=False))
        items = pd.DataFrame(items_structure)
        items_json = items.to_json(orient='records')
        aio.send_data(feed.key, items_json)
    
    return items
    
    

# Adafruit connector taken from lab exercises
"""


#----ACCESS OR CREATE FEED
# access or create a feed with a given key or name
try: # access the feed with key 'button' if it exists
    feed = aio.feeds('button')
except RequestError: # create a 'button' (name, key) feed otherwise
    feed = aio.create_feed(Feed(name='button', key='button', history=False))


#----SEND/POST DATA TO FEED
# define a function that sends the latest data for a feed identified by key
def button_status_send_data(key, data):
    return aio.send_data(key, data)

# add the data value of the Button status to the feed, identified by its key

button_status = 0
try:
    while True:
        # button_status = int(eh.input.one.read())
        ## conditional expression 
        ## uncomment for button managed via gpiozero/explorerhat
        # button_status = 1 if button.is_pressed else 0
        button_status = 1 if randrange(0,2) == 1 else 0
        button_status_send_data(feed.key, button_status)
        time.sleep(2)
except KeyboardInterrupt:
    print('bye')
finally:
    print('game over')


"""