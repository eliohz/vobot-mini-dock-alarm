import lvgl as lv
import peripherals
import asyncio
import urequests  # For HTTP requests in MicroPython

# Application metadata
NAME = "Ticket Counter"
CAN_BE_AUTO_SWITCHED = True

# Global variables
scr = None
label = None
API_URL = "https://api.mcsrvstat.us/3/gommehd.net"  # API endpoint

# Acquire ambient light
peripherals.ambient_light.acquire()

async def fetch_ticket_number():
    """Fetch the simulated ticket number (player count) from the API."""
    try:
        response = urequests.get(API_URL)
        data = response.json()
        return data.get("players", {}).get("online", 0)  # Get 'online' from 'players'
    except Exception as e:
        print(f"Error fetching data: {e}")
        return -1  # Return -1 in case of error

async def on_running_foreground():
    """Called when the app is active, approximately every 200ms."""
    global label

    # Fetch the ticket number (player count)
    ticket_number = await fetch_ticket_number()

    # Update label with the ticket number
    if ticket_number >= 0:
        label.set_text(f"Anzahl Tickets: #{ticket_number}")
    else:
        label.set_text("Error fetching data")

    # Update ambient light based on ticket number
    if ticket_number >= 20:
        peripherals.ambient_light.set_color([(255, 0, 0)], True)  # Red
    elif ticket_number >= 10:
        peripherals.ambient_light.set_color([(255, 255, 0)], True)  # Yellow
    else:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)  # Green

    await asyncio.sleep(1)  # Delay for 1 second

async def on_stop():
    """Called when the app is stopped or closed."""
    global scr
    if scr:
        scr.clean()
        del scr

    # Release ambient light
    peripherals.ambient_light.release()

async def on_start():
    """Called when the app starts."""
    global scr, label

    # Create a new screen and label
    scr = lv.obj()
    label = lv.label(scr)
    label.center()
    label.set_text("Fetching ticket number...")

    # Load the screen
    lv.scr_load(scr)
