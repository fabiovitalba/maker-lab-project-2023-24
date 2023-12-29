import time
from Adafruit_IO import Client, Data, Feed, RequestError
from env import adafruit_user, adafruit_key

# create an instance of the REST client.
aio = Client(adafruit_user, adafruit_key)

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