from const import ITEMS_KEY
from adafruit_connector import read_items, add_item
from datetime import datetime

# In order to retrieve the existing items from adafruit, we need to call the read_items method from adafruit
items = read_items(ITEMS_KEY)

# In order to add a new Item to the set, we need to initialize a List (Array) with the new data and call the add_item() method.
# The List is in format [timestamp, barcode, description, expiration_date, quantity, datetime_created, datetime_modified]
new_item = [datetime.now(), 'barcode', 'description', 'expiration date', 1, datetime.now(), None]
if not add_item(ITEMS_KEY,items,new_item):
    print('\033[91mADD_ITEM-method FAILED\033[0m')

# Read items from Adafruit again in order to compare the cloud data with the local data
items_updated = read_items(ITEMS_KEY)
print('##### ADAFRUIT #####')
print(items_updated)
print('\n##### LOCAL ####')
print(items)

# Test result for cloud/local data equality
# Text Color: \033[94m=BLUE, \033[91m=RED, \033[92m=GREEN, \033[0m=DEFAULT
print('\n\033[94mTEST: Adafruit Items Read & Add: \033[0m')
if len(items_updated) != len(items):
    print('\033[91mUNALIGNED\033[0m')
else:
    print('\033[92mOK\033[0m')
