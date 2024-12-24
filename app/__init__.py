import lvgl as lv
import peripherals
import asyncio
import urequests

NAME = "Ticket Counter"
CAN_BE_AUTO_SWITCHED = True

scr = None
label = None
API_URL = "https://api.mcsrvstat.us/3/gommehd.net"
last_ticket_number = 0

peripherals.ambient_light.acquire()

async def fetch_ticket_number():
    """Fetch the simulated ticket number (player count) with retries."""
    global last_ticket_number
    retries = 3
    for attempt in range(retries):
        try:
            response = urequests.get(API_URL)
            data = response.json()
            last_ticket_number = data.get("players", {}).get("online", 0)
            return last_ticket_number
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(2)  # Wait before retrying
    return last_ticket_number  # Fallback to cached value

async def on_running_foreground():
    global label

    ticket_number = await fetch_ticket_number()
    label.set_text(f"Anzahl Tickets: #{ticket_number}")

    if ticket_number >= 20:
        peripherals.ambient_light.set_color([(255, 0, 0)], True)
    elif ticket_number >= 10:
        peripherals.ambient_light.set_color([(255, 255, 0)], True)
    else:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)

    await asyncio.sleep(10)  # Delay for 10 seconds

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
    label.set_text("Fetching ticket number...")
    lv.scr_load(scr)
