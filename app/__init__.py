import lvgl as lv
import peripherals
import asyncio
import urequests  # For HTTP requests in MicroPython

NAME = "Ticket Counter"
CAN_BE_AUTO_SWITCHED = True

# Global variables
scr = None
label = None
API_URL = "https://catfact.ninja/fact"  # API endpoint
last_ticket_number = 0

# Acquire ambient light
peripherals.ambient_light.acquire()

async def fetch_ticket_number():
    """Fetch the ticket number (fact length) from the Cat Fact API."""
    global last_ticket_number
    retries = 3
    for attempt in range(retries):
        try:
            response = urequests.get(API_URL)
            data = response.json()
            last_ticket_number = data.get("length", 0)  # Get the length of the fact
            return last_ticket_number
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(2)  # Wait before retrying
    return last_ticket_number  # Fallback to cached value

async def on_running_foreground():
    """Called when the app is active, approximately every 200ms."""
    global label

    ticket_number = await fetch_ticket_number()
    label.set_text(f"Anzahl Tickets: #{ticket_number}")

    # Update ambient light based on ticket number
    if ticket_number >= 100:
        peripherals.ambient_light.set_color([(255, 0, 0)], True)  # Red
    elif ticket_number >= 50:
        peripherals.ambient_light.set_color([(255, 255, 0)], True)  # Yellow
    else:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)  # Green

    await asyncio.sleep(10)  # Delay for 10 seconds to respect API rate limits

async def on_stop():
    """Called when the app is stopped or closed."""
    global scr
    if scr:
        scr.clean()
        del scr
    peripherals.ambient_light.release()

async def on_start():
    """Called when the app starts."""
    global scr, label
    scr = lv.obj()
    label = lv.label(scr)
    label.center()
    label.set_text("Fetching ticket number...")
    lv.scr_load(scr)
