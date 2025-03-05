
# **1. Project Description**  
**Vobot Ticket Alarm** is a holiday project that uses the Vobot MiniDock to indicate the status of an API (true or false). This can be used for various applications, such as an alarm system.

# **2. Dependencies (Requirements)**  
- Vobot MiniDock  
- Selfhosted API Servuice that can be either true or false
- Python (Micropython)  
- lvgl Library  
- urequests Library  
- peripherials Library  

# **3. Architecture Overview**  
The project consists of the following main components
```
├── Alarm
│   ├── __init__.py        # MicroPython application logic
│   ├── manifest.yml       # Metadata for initializing the app
│   └── resources          # Assets for display and UI
│       ├── false.jpg      # Image shown when bool on API == false
│       ├── icon.png       # App icon
│       └── true.jpg       # Image shown when bool on API == true
└── README.md              # Project documentation

```

# **4. System Structure**
```bash

       +-------------------------------+
       |  Trigger (HTTP POST Request)  | 
       +-------------------------------+
                       |
                       | POST (false)
                       v
         +----------------------------+
         |  Self-Hosted API (Boolean) |  https://your-api.com/api/ticket-status
         +------------+---------------+
                   Ʌ     |
  Button pressed   |     |  GET Request
  POST (true)      |     |
                   |     v
  +-------------------------------------------+
  |                  VoBot                    |
  |  [Green (if True)] <--> [Red (if False)]  |
  +---------+---------------------------------+
```

# **5. Installation**  
To install and configure the Vobot system, please follow the official guide at [dock.myvobot.com](https://dock.myvobot.com/developer/getting_started/).  

Steps:  
1. Install [Thonny](https://thonny.org/)  
2. Connect to ESP32  
3. Copy the `App` folder to the ESP32  
4. Execute `manifest.yml`  

# **6. Usage / Testing**  
- When the API returns `true`, the light/display turns **green**.
- When the API returns `false`, the light/display turns **red**.
- If the Vobot is **red**, it can be reset to **green** by pressing the button.

## **7. Manually Updating API Boolean (POST Request)**  
The project uses a **self-hosted API** that maintains a boolean value (`true` or `false`).  

**Using cURL (Linux/macOS/Windows)**
```bash
curl -X POST https://your-api.com/api/ticket-status -H "Content-Type: application/json" -d '{"status": false}'
curl -X POST https://your-api.com/api/ticket-status -H "Content-Type: application/json" -d '{"status": true}'
```
**Using PowerShell (Windows)**
```powershell
Invoke-WebRequest -Uri "https://your-api.com/api/ticket-status" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"status": false}'
Invoke-WebRequest -Uri "https://your-api.com/api/ticket-status" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"status": true}'
```
