import lvgl as lv
import peripherals
import time

NAME = "Ticket Counter"
CAN_BE_AUTO_SWITCHED = True
ticket_number = 0 

scr = lv.obj()
label = None

peripherals.ambient_light.acquire()

font = lv.font_montserrat_40 

async def on_running_foreground():
    """Called when the app is active, approximately every 200ms."""
    global ticket_number
    ticket_number += 1
    
    label.set_text(f'Anzahl Tickets: #{ticket_number}')
    
    if ticket_number >= 20:
        peripherals.ambient_light.set_color([(255, 0, 0)], True)
    elif ticket_number >= 10:
        peripherals.ambient_light.set_color([(255, 255, 0)], True)
    else:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)

    time.sleep(1)

async def on_stop():
    """Called when the app is stopped or closed."""
    global ticket_number
    ticket_number = 0 
    peripherals.ambient_light.release()
    scr.clean() 

async def on_start():
    global label
    
    label = lv.label(scr)
    label.center()
    label.set_text('BPOS')

    lv.scr_load(scr)

