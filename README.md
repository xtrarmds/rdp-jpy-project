RDP JPY Project
A FastAPI-based web application for real-time currency pair data (e.g., XAU=, JPY=) using LSEG data streams.
Features

Input multiple currency pairs via input.html.
Display real-time data in a stable table with fixed 4-decimal places and column widths.
Supports WebSocket (display.html) and HTTP polling (display_http.html).
Optimized logging with rotation to prevent disk overflow.

Project Structure

main.py: FastAPI backend with WebSocket and HTTP endpoints.
input.html: Input page for currency pairs.
display.html: Display page with WebSocket.
display_http.html: Display page with HTTP polling (fallback for WebSocket issues).
static/: JavaScript libraries (React, Tailwind CSS).
requirements.txt: Python dependencies.

Prerequisites

Python 3.8+
Git
LSEG Data Platform credentials (for lseg-data.config.json)

Setup

Clone the repository:
git clone https://github.com/your-username/rdp-jpy-project.git
cd rdp-jpy-project


Create and activate virtual environment:
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows


Install dependencies:
pip install -r requirements.txt

Note: If lseg-data fails, contact LSEG for access or configure a private PyPI source.

Configure LSEG credentials:

Create lseg-data.config.json with your credentials:{
    "username": "your-username",
    "password": "your-password",
    "client_id": "your-client-id"
}




Run the server:
uvicorn main:app --host 0.0.0.0 --port 8000

Or run in background:
nohup uvicorn main:app --host 0.0.0.0 --port 8000 >> uvicorn.log 2>&1 &


Access the application:

Open http://localhost:8000/input in a browser.
Input currency pairs (e.g., XAU=, JPY=), submit, and view data at http://localhost:8000/display.
Use http://localhost:8000/display_http for HTTP polling if WebSocket fails (e.g., due to firewall).



Notes

Ensure port 8000 is open (sudo ufw allow 8000 on Linux, or disable firewall on Windows).
Logs are stored in lseg-data-lib.log with rotation (max 50MB).
For remote access, check network and firewall settings.

License
MIT License

