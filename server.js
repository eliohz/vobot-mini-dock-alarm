const express = require('express');
const app = express();
app.use(express.json());

let ticketStatus = false; // Default status

// Log server startup
console.log("Starting server...");

// Endpoint to get ticket status
app.get('/api/ticket-status', (req, res) => {
    console.log("GET /api/ticket-status called");
    res.json({ status: ticketStatus });
});

// Endpoint to update ticket status
app.post('/api/ticket-status', (req, res) => {
    console.log("POST /api/ticket-status called with body:", req.body);

    const { status } = req.body;
    if (typeof status === 'boolean') {
        ticketStatus = status;
        res.json({ message: 'Status updated successfully', status: ticketStatus });
    } else {
        res.status(400).json({ error: 'Invalid status value' });
    }
});

// Start the server
const PORT = 4000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));