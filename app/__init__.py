import lvgl as lv
import urequests
import peripherals

# Constants and configuration
NAME = "BPOS Alarm"
API_URL = "https://eliohz.com/api/ticket-status"
CAN_BE_AUTO_SWITCHED = True
DEFAULT_BG_COLOR = lv.color_hex3(0x000)

# Global variables
scr = None  # LVGL screen object
label = None  # LVGL label object for displaying status
last_ticket_status = False  # Tracks the last fetched ticket status

# Acquire the peripheral for ambient light control
peripherals.ambient_light.acquire()

async def fetch_ticket_status():
    # Fetches the ticket status from the API.
    global last_ticket_status
    retries = 3  # Number of retry attempts

    for attempt in range(retries):
        try:
            # Make an HTTP GET request to the API
            response = urequests.get(API_URL)
            response_data = response.json()
            last_ticket_status = response_data.get("status", False)
            return last_ticket_status
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

    # Return the last known ticket status if all retries fail
    return last_ticket_status

async def on_running_foreground():
    # Updates the screen and ambient light based on the ticket status.
    global label

    ticket_status = await fetch_ticket_status()
    
    # Update label text and ambient light color based on the ticket status
    if ticket_status:
        label.set_text("KEINE NEUEN TICKETS")
        peripherals.ambient_light.set_color([(0, 255, 0)], True)  # Green
    else:
        label.set_text("NEUES TICKET!")
        peripherals.ambient_light.set_color([(255, 0, 0)], True)  # Red

def send_post_request():
    # Sends a POST request to the API to update the status.
    data = {'status': True}
    urequests.post(API_URL, json=data)

def event_handler(event):
    # Handles LVGL events such as key presses.
    e_code = event.get_code()

    if e_code == lv.EVENT.KEY:
        e_key = event.get_key()

        # Handle specific key events
        if e_key == lv.KEY.ENTER:
            send_post_request()

    elif e_code == lv.EVENT.FOCUSED:
        # Enable editing mode if not already in edit mode
        if not lv.group_get_default().get_editing():
            lv.group_get_default().set_editing(True)

async def on_stop():
    # Cleans up the LVGL screen when the app stops.
    global scr
    print('on stop')
    if scr:
        scr.clean()
        scr.del_async()
        scr = None

async def on_start():
    # Initializes the LVGL screen and starts the app.
    global scr, label
    print('on start')

    # Create a new screen and label
    scr = lv.obj()
    label = lv.label(scr)
    label.center()
    label.set_text("Fetching ticket status...")
    lv.scr_load(scr)

    # Set the screen background color
    scr.set_style_bg_color(DEFAULT_BG_COLOR, lv.PART.MAIN)

    # Fetch the ticket status asynchronously
    await fetch_ticket_status()

    # Attach the event handler to the screen
    scr.add_event(event_handler, lv.EVENT.ALL, None)

    # Focus the key operation on the current screen and enable editing mode
    lv.group_get_default().add_obj(scr)
    lv.group_focus_obj(scr)
    lv.group_get_default().set_editing(True)
