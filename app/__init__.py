import lvgl as lv
import peripherals
import asyncio
import urequests

NAME = "Ticket Counter"
CAN_BE_AUTO_SWITCHED = True

scr = None
label = None
API_URL = "https://eliohz.com/api/ticket-status"
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
            await asyncio.sleep(2) 
    return last_ticket_status

# SOLLTE FUNKTIONIEREN
async def send_post_request():
    try:
        payload = {
            "type": "Http",
            "inputs": {
                "uri": API_URL,
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    "status": True
                }
            }
        }
        response = urequests.post(API_URL, json=payload)
        print(f"POST response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending POST request: {e}")

async def on_running_foreground():
    global label

    ticket_status = await fetch_ticket_status()
    if ticket_status:
        label.set_text("KEINE NEUEN TICKETS")
        peripherals.ambient_light.set_color([(0, 255, 0)], True)  # Green
    else:
        label.set_text("NEUES TICKET!")
        peripherals.ambient_light.set_color([(255, 0, 0)], True)  # Red

    await asyncio.sleep(3)

# DAS GEHT NICHT!!!
def event_handler(e):
    if e_key == lv.KEY.ENTER:
        asyncio.create_task(send_post_request())

async def on_stop():
    global scr
    if scr:
        scr.clean()
        del scr
    peripherals.ambient_light.release()

async def on_start():
    global scr, label
    scr = lv.obj()
    label = lv.label(scr)
    label.center()
    label.set_text("Fetching ticket status...")
    lv.scr_load(scr)

    # DAS GEHT NICHT!!!
    scr.add_event_cb(event_handler, lv.EVENT.KEY, None)

    # HIER NICHT SICHER???
    await on_running_foreground() 
