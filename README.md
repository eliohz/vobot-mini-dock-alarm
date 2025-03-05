Here is your project description in English with the requested changes:  

---

# **1. Project Description**  
**Vobot Ticket Alarm** is a holiday project that utilizes the Vobot MiniDock to indicate whether new tickets are available in the N&S queue.  

---

# **2. Dependencies (Requirements)**  
- Vobot MiniDock  
- Selfhosted API Servuice that can be either true or false
- Python (Micropython)  
- lvgl Library  
- urequests Library  
- peripherials Library  

---

# **3. Installation**  
To install and configure the Vobot system, please follow the official guide at [dock.myvobot.com](https://dock.myvobot.com/developer/getting_started/).  

Steps:  
1. Install [Thonny](https://thonny.org/)  
2. Connect to ESP32  
3. Copy the `App` folder to the ESP32  
4. Execute `manifest.yml`  

---

# **4. Usage / Testing**  
## **1. Usage**  
- When a new ticket arrives, the light turns **red**.  
- After viewing the ticket, it can be confirmed using a button, turning the light **green**.  

## **2. Manually Updating API Boolean (POST Request)**  
The project uses a **self-hosted API** that maintains a boolean value (`true` or `false`).  

### **Using cURL (Linux/macOS/Windows)**
```bash
curl -X POST https://your-api.com/api/ticket-status -H "Content-Type: application/json" -d '{"status": false}'
curl -X POST https://your-api.com/api/ticket-status -H "Content-Type: application/json" -d '{"status": true}'
```
### **Using PowerShell (Windows)**
```powershell
Invoke-WebRequest -Uri "https://your-api.com/api/ticket-status" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"status": false}'
Invoke-WebRequest -Uri "https://your-api.com/api/ticket-status" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"status": true}'
```

---

# **5. Architecture Overview**  
The project consists of the following main components:  
```markdown
`BPOS/`
  `manifest.yml`: Metadata for the project, required for initializing the app.
  `__init__.py__`: MicroPython code for the application.
  `resources/`: Assets such as app icons and display images (new ticket/no new tickets).
```

---

# **6. System Structure**
```markdown
          +------------------------+
          |    BPOS Chat (Queue)   |
          +-----------+------------+
                      |
                      | "forwarded" in text
                      v
   +---------------------------------------+
   |  Power Automate Task (Trigger Event)  | 
   +---------------------------------------+
                      |
                      | POST (False)
                      v
         +----------------------------+
         |  Self-Hosted API (Boolean) |  https://your-api.com/api/ticket-status
         +------------+---------------+
                   Ʌ     |
  Button pressed   |     |  GET Request
  POST (True)      |     |
                   |     v
  +-------------------------------------------+
  |                VoBot                      |
  |  [Green (if True)] <--> [Red (if False)]  |
  +---------+---------------------------------+
```

# **7. Project Structure**

The project is organized as follows:

```
.
├── BPoS
│   ├── __init__.py        # MicroPython application logic
│   ├── manifest.yml       # Metadata for initializing the app
│   └── resources          # Assets for display and UI
│       ├── false.jpg      # Image shown when no new tickets are available
│       ├── icon.png       # App icon
│       └── true.jpg       # Image shown when a new ticket is available
└── README.md              # Project documentation
```