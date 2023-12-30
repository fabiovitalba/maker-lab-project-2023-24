from Adafruit_IO import Client, Feed, RequestError
from datetime import datetime
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

def update_items_in_adafruit(items_df):
    # create an instance of the REST client.
    aio = Client(adafruit_user, adafruit_key)

    # add item to the adafruit item table
    try:
        feed = aio.feeds(ITEMS_KEY)
        items_json = items_df.to_json(orient='records')
        aio.send_data(feed.key, items_json)
        return True
    except RequestError:
        return False

def add_item(items_df, item):
    barcodes = items_df['Barcode']
    if barcodes.isin([item[1]]).any():
        return reduce_item(items_df, item[1], -item[4])
    else:
        items_df.loc[len(items_df)] = item
        return update_items_in_adafruit(items_df)

def reduce_item(items_df, barcode, quantity_diff):
    items_df.loc[items_df['Barcode'] == barcode, 'Quantity'] -= quantity_diff
    items_df.loc[items_df['Barcode'] == barcode, 'Date modified'] = datetime.now()
    if (items_df.loc[items_df['Barcode'] == barcode, 'Quantity'].all() <= 0):
        remove_item(items_df, barcode)
    return update_items_in_adafruit(items_df)

def remove_item(items_df, barcode):
    items_df = items_df[items_df['Barcode'] != barcode]
    return update_items_in_adafruit(items_df)
# endregion Items-methods
