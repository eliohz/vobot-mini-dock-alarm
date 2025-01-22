## 1. Projektbeschreibung
**Vobot Ticket Alarm** ist ein Ferienprojekt, das die Vobot MiniDock nutzt, um ein einfacher Ticket Alarm

## 2. Dependencies (Voraussetzungen)
- Vobot MiniDock
- Python (Micropython)
- lvgl Library
- urequests Library
- peripherials Libary

## 3. Installation
1. Für die Installation und Konfiguration des Vobot-Systems folgen Sie bitte der offiziellen Anleitung auf [dock.myvobot.com](https://dock.myvobot.com/developer/getting_started/).

- [Thonny](https://thonny.org/) installieren
- Mit ESP32 verbinden
- App Ordner auf den ESP32 kopieren.
- Ausführen manifest.yml

## 4 Architektur
```
          +------------------------+
          |    BPOS Chat (Queue)   |
          +-----------+------------+
                      |
                      | "weitergeleitet" im Text
                      v
   +---------------------------------------+
   |  Power Automate Task (Trigger Event)  |
   +---------------------------------------+
                      |
                      | POST  (False)
                      v
         +-------------------------+
         |   eliohz.com (API Bool) |
         +------------+------------+
                   Ʌ     |
  Knopf gedrückt   |     |  GET Request
  POST (True)      |     |
                   |     v
  +----------------------------------------+
  |                VoBot                   |
  |  [Grün(if True)] <--> [Rot(if False)]  |
  +---------+------------------------------+
   
```

## 5 Nutzung / Testing
1. Nutzung
- Wenn Ticket reinkommt, wird das Licht auf Rot gestellt.
- Wenn Ticket angeschaut wurde, kann mit Knopf bestätigt werden. Das Licht wird auf Grün gestellt.

2. API Boolean Manuell bearbeiten (POST Request)
    ```bash 
    curl -X POST https://eliohz.com/api/ticket-status   -H "Content-Type: application/json"   -d '{"status": false}'
    curl -X POST https://eliohz.com/api/ticket-status   -H "Content-Type: application/json"   -d '{"status": true}'
    ```
    ```powershell
    Invoke-WebRequest -Uri "https://eliohz.com/api/ticket-status" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"status": false}'
    Invoke-WebRequest -Uri "https://eliohz.com/api/ticket-status" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"status": true}'
    ```

## 6 Architekturübersicht
Das Projekt besteht aus den folgenden Hauptkomponenten:
- `manifest.yml`: Metadaten für das Projekt. Wird benötigt um die App zu initialisieren.
- `__init.py__`: MicroPython Code für App.
- `ressources/`: Ressourcen. (App Icon/Display Bild "neues Ticket und keine neuen Tickets")

## 7 Kontaktinformationen
Hauptverantwortlicher: Elio Heinz
E-Mail: elio.heinz@bechtle.com