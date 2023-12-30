from Adafruit_IO import Client, Feed, RequestError
from io import StringIO
from const import ITEMS_KEY
from env import adafruit_user, adafruit_key
import pandas as pd

# region Items-methods
items_structure = {
    'Timestamp': [],
    'Barcode': [],
    'Description': [],
    'Expiration Date': [],
    'Quantity': [],
    'Date added': [],
    'Date modified': []
}

def read_items():
    # create an instance of the REST client.
    aio = Client(adafruit_user, adafruit_key)

    # Access existing or create new FEED using the name/key passed as parameter
    try:
        # Open Adafruit Feed, retrieve its data (which is in JSON format), create DataFrame from the JSON
        feed = aio.feeds(ITEMS_KEY)
        feed_data = aio.receive(feed.key)
        items = pd.read_json(StringIO(feed_data.value))
    except RequestError:
        # If an error is thrown, we assume the Adafruit Feed does not exist
        # In this case we create a new Adafruit Feed, a new DataFrame using the predefined Structure, and store the new DataFrame in Adafruit
        feed = aio.create_feed(Feed(name=ITEMS_KEY, key=ITEMS_KEY, history=False))
        items = pd.DataFrame(items_structure)
        items_json = items.to_json(orient='records')
        aio.send_data(feed.key, items_json)
    
    return items

def add_item(items_df, item):
    # create an instance of the REST client.
    aio = Client(adafruit_user, adafruit_key)

    # add item to the adafruit item table
    try:
        feed = aio.feeds(ITEMS_KEY)

        # TODO: Verify if the barcode is already present. in which case we increment the quantity
        items_df.loc[len(items_df)] = item
        items_json = items_df.to_json(orient='records')
        aio.send_data(feed.key, items_json)
        return True
    except RequestError:
        return False

def reduce_item(items_df, barcode, quantity_diff):
    return False #TODO: Implement method that reduces the quantity of an existing item by the provided quantity_diff

def remove_item(items_df, barcode):
    return False #TODO: Remove the whole item-entry of the provided barcode
# endregion Items-methods
