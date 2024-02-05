from Adafruit_IO import Client, Feed, RequestError
from io import StringIO
from const import ITEMS_KEY, BARCODE_LBL, DESC_LBL, EXP_LBL, QTY_LBL, DATE_ADDED_LBL
from env import adafruit_user, adafruit_key
import pandas as pd

# region Items-methods
items_structure = {
    BARCODE_LBL: [],
    DESC_LBL: [],
    EXP_LBL: [],
    QTY_LBL: [],
    DATE_ADDED_LBL: []
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

        if len(items) <= 0:
            items = pd.DataFrame(items_structure)
        else:
            # Since read_json converts all columns to datatype object, we need to manually convert all values again
            items[BARCODE_LBL] = items[BARCODE_LBL].astype(str)
            items[DESC_LBL] = items[DESC_LBL].astype(str)
            # pd.to_datetime(items[EXP_LBL], dayfirst=False)
            items[EXP_LBL] = items[EXP_LBL].astype(int)
            items[QTY_LBL] = items[QTY_LBL].astype(float)
            # pd.to_datetime(items[DATE_ADDED_LBL], dayfirst=False)
            items[DATE_ADDED_LBL] = items[DATE_ADDED_LBL].astype(int)

    except RequestError:
        # If an error is thrown, we assume the Adafruit Feed does not exist
        # In this case we create a new Adafruit Feed, a new DataFrame using the predefined Structure, and store the new DataFrame in Adafruit
        feed = aio.create_feed(
            Feed(name=ITEMS_KEY, key=ITEMS_KEY, history=False))
        items = pd.DataFrame(items_structure)
        items_json = items.to_json(
            orient="records", date_format="iso", default_handler=str)
        aio.send_data(feed.key, items_json)

    return items


def update_items_in_adafruit(items_df):
    # create an instance of the REST client.
    aio = Client(adafruit_user, adafruit_key)

    # add item to the adafruit item table
    try:
        feed = aio.feeds(ITEMS_KEY)
        items_json = items_df.to_json(
            orient="records", date_format="iso", default_handler=str)
        aio.send_data(feed.key, items_json)
        return True
    except RequestError:
        return False


def add_item(items_df, item):
    # We verify that each column uses the correct data type or convert it if required
    # | Barcode | Description | Exp. Date | Quantity | Date Added |
    item[0] = str(item[0])
    item[1] = str(item[1])
    item[2] = int(item[2])  # Unix Timestamp
    item[3] = float(item[3])
    item[4] = int(item[4])

    items_df.loc[len(items_df)] = item

    return update_items_in_adafruit(items_df)


def remove_item(items_df, row_index, quantity):
    current_quantity = items_df.loc[row_index, QTY_LBL]

    if quantity >= current_quantity:
        # Remove the entire row if the specified quantity is greater or equal to the current quantity
        items_df.drop(row_index, inplace=True)
    else:
        # Subtract the specified quantity from the current quantity
        items_df.loc[row_index, QTY_LBL] -= quantity

    return update_items_in_adafruit(items_df)
# endregion Items-methods
