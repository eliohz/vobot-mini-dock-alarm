# Vobot MiniDock Ticket Alarm

**Vobot Ticket Alarm** ist ein Ferienprojekt, das die Vobot MiniDock nutzt, um ein einfacher Ticket Alarm
## Funktionen
- **Ticketanzeige**: Zeigt an wenn ein neues Ticket reinkommt
- **Umgebungslichtsteuerung**: Farbänderung wenn Ticket reinkommt
- **Einfache Nutzung**: Nutzer können per knopfdruck bestätigen wenn sie das ticket angeschaut haben.

## Installation und Konfiguration
Für die Installation und Konfiguration des Vobot-Systems folgen Sie bitte der offiziellen Anleitung auf [dock.myvobot.com](https://dock.myvobot.com/developer/getting_started/).

## Load code to Device with Thonny
Download [Thonny](https://thonny.org/)

app -> MicroPython device /apps -> run manifest.yml

## Edit Bool (API)
curl -X POST https://eliohz.com/api/ticket-status   -H "Content-Type: application/json"   -d '{"status": false}'

curl -X POST https://eliohz.com/api/ticket-status   -H "Content-Type: application/json"   -d '{"status": true}'
