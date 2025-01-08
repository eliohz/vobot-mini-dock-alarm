import lvgl as lv
import urequests
import peripherals
 
# Variables
NAME = "BPOS Alarm"
API_URL = "https://eliohz.com/api/ticket-status"
CAN_BE_AUTO_SWITCHED = True
 
# LVGL widgets
scr = None
label = None
DEFAULT_BG_COLOR = lv.color_hex3(0x000)
last_ticket_status = False
 
# Acquire the peripheral for ambient light control
peripherals.ambient_light.acquire()
 
async def fetch_ticket_status():
    """Fetches the ticket status from the API."""
    global last_ticket_status
    retries = 3
    for attempt in range(retries):
        try:
            response = urequests.get(API_URL)
            response_data = response.json()
            last_ticket_status = response_data.get("status", False)
            return last_ticket_status
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
    return last_ticket_status
 
async def on_running_foreground():
    global label
 
    ticket_status = await fetch_ticket_status()
    if ticket_status:
        label.set_text("KEINE NEUEN TICKETS")
        peripherals.ambient_light.set_color([(0, 255, 0)], True)  # Green
    else:
        label.set_text("NEUES TICKET!")
        peripherals.ambient_light.set_color([(255, 0, 0)], True)  # Red
 
def send_post_request():
    myobj = {'status': True}
    urequests.post(API_URL,json = myobj)
 
def event_handler(event):
    e_code = event.get_code()
    if e_code == lv.EVENT.KEY:
        e_key = event.get_key()
        #if e_key == lv.KEY.RIGHT:
            #send_post_request()
        #elif e_key == lv.KEY.LEFT:
            #send_post_request()
        if e_key == lv.KEY.ENTER:
            send_post_request()
    elif e_code == lv.EVENT.FOCUSED:
        # If not in edit mode, set to edit mode.
        if not lv.group_get_default().get_editing():
            lv.group_get_default().set_editing(True)
 
async def on_stop():
    print('on stop')
    global scr
    if scr:
        scr.clean()
        scr.del_async()
        scr = None
 
async def on_start():
    print('on start')
    global scr, label
    scr = lv.obj()
    label = lv.label(scr)
    label.center()
    label.set_text("Fetching ticket status...")
    lv.scr_load(scr)
 
    scr.set_style_bg_color(DEFAULT_BG_COLOR, lv.PART.MAIN)
    fetch_ticket_status()
   
    scr.add_event(event_handler, lv.EVENT.ALL, None)
 
    # Focus the key operation on the current screen and enable editing mode.
    lv.group_get_default().add_obj(scr)
    lv.group_focus_obj(scr)
    lv.group_get_default().set_editing(True)
