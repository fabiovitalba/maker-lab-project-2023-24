from adafruit_connector import read_items, add_item, reduce_item, remove_item
from datetime import datetime
# Text Color: \033[94m=BLUE, \033[91m=RED, \033[92m=GREEN, \033[0m=DEFAULT

# In order to retrieve the existing items from adafruit, we need to call the read_items method from adafruit
items = read_items()
start_len = len(items)

# In order to add a new Item to the set, we need to initialize a List (Array) with the new data and call the add_item() method.
# The List is in format [timestamp, barcode, description, expiration_date, quantity, datetime_created, datetime_modified]
new_item = [datetime.now(), '8056149086957', 'Olive Nere Denocciolate in Salamoia', '31/12/2024', 3, datetime.now(), None]
if not add_item(items, new_item):
    print('\033[91mADD_ITEM-method FAILED\033[0m')
new_item = [datetime.now(), '8001300242802', 'Maionese vegetale', '31/07/2024', 2, datetime.now(), None]
if not add_item(items, new_item):
    print('\033[91mADD_ITEM-method FAILED\033[0m')

# Read items from Adafruit again in order to compare the cloud data with the local data
items_updated = read_items()
# Test result for cloud/local data equality
print('\n\033[94m1. TEST: Adafruit Items Read & Add: \033[0m')
if (len(items_updated) != len(items)) or (len(items_updated) != start_len + 2):
    print('\033[91mFAIL\033[0m')
else:
    print('\033[92mOK\033[0m')

print(items_updated)

reduce_item(items, '8056149086957', 2)
print('\n\033[94m2. TEST: Adafruit Items Reduce > 0: \033[0m')
if len(items) != start_len + 2:
    print('\033[91mFAIL\033[0m')
else:
    print('\033[92mOK\033[0m')

print(items_updated)

reduce_item(items, '8001300242802', 2)
print('\n\033[94m3. TEST: Adafruit Items Reduce <= 0: \033[0m')
if len(items) != start_len + 1:
    print('\033[91mFAIL\033[0m')
else:
    print('\033[92mOK\033[0m')

print(items_updated)

remove_item(items, '8056149086957')
print('\n\033[94m4. TEST: Adafruit Items Remove: \033[0m')
if len(items) != start_len:
    print('\033[91mFAIL\033[0m')
else:
    print('\033[92mOK\033[0m')

print(items_updated)
