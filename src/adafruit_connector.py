from Adafruit_IO import Client, Feed, RequestError
from io import StringIO
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
        items = pd.read_json(StringIO(feed_data.value))
    except RequestError:
        # If an error is thrown, we assume the Adafruit Feed does not exist
        # In this case we create a new Adafruit Feed, a new DataFrame using the predefined Structure, and store the new DataFrame in Adafruit
        feed = aio.create_feed(Feed(name=key, key=key, history=False))
        items = pd.DataFrame(items_structure)
        items_json = items.to_json(orient='records')
        aio.send_data(feed.key, items_json)
    
    return items

def add_item(key, items_df, item):
    # create an instance of the REST client.
    aio = Client(adafruit_user, adafruit_key)

    # add item to the adafruit item table
    try:
        feed = aio.feeds(key)

        items_df.loc[len(items_df)] = item
        items_json = items_df.to_json(orient='records')
        aio.send_data(feed.key, items_json)
        return True
    except RequestError:
        return False
