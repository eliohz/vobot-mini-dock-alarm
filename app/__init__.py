import lvgl as lv
import peripherals
import asyncio

# Application metadata
NAME = "Ticket Counter"
CAN_BE_AUTO_SWITCHED = True

# Global variables
ticket_number = 0
scr = None
label = None

# Acquire ambient light
peripherals.ambient_light.acquire()

# Define the on_running_foreground lifecycle
async def on_running_foreground():
    """Called when the app is active, approximately every 200ms."""
    global ticket_number

    ticket_number += 1
    label.set_text(f"Anzahl Tickets: #{ticket_number}")

    # Update ambient light based on ticket count
    if ticket_number >= 20:
        peripherals.ambient_light.set_color([(255, 0, 0)], True)  # Red
    elif ticket_number >= 10:
        peripherals.ambient_light.set_color([(255, 255, 0)], True)  # Yellow
    else:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)  # Green

    await asyncio.sleep(0.2)  # Use asyncio sleep instead of time.sleep

# Define the on_stop lifecycle
async def on_stop():
    """Called when the app is stopped or closed."""
    global scr, ticket_number
    ticket_number = 0

    if scr:
        scr.clean()
        del scr

    # Release ambient light
    peripherals.ambient_light.release()

# Define the on_start lifecycle
async def on_start():
    """Called when the app starts."""
    global scr, label

    # Create a new screen and label
    scr = lv.obj()
    label = lv.label(scr)
    label.center()
    label.set_text("BPOS")

    # Load the screen
    lv.scr_load(scr)
