# RDP JPY Project

A FastAPI-based web application for real-time currency pair data (e.g., XAU=, JPY=) using LSEG data streams.

## Features
- Input multiple currency pairs via `input.html`.
- Display real-time data in a stable table with fixed 4-decimal places and column widths.
- Supports WebSocket (`display.html`) and HTTP polling (`display_http.html`).
- Optimized logging with rotation to prevent disk overflow.

## Project Structure
- `main.py`: FastAPI backend with WebSocket and HTTP endpoints.
- `input.html`: Input page for currency pairs.
- `display.html`: Display page with WebSocket.
- `display_http.html`: Display page with HTTP polling (fallback for WebSocket issues).
- `static/`: JavaScript libraries (React, Tailwind CSS).
- `requirements.txt`: Python dependencies.

## Prerequisites
- Python 3.8+
- Git
- LSEG Data Platform credentials (for `lseg-data.config.json`)

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/xtrarmds/rdp-jpy-project.git
   cd rdp-jpy-project
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Note: If `lseg-data` fails, contact LSEG for access or configure a private PyPI source.

4. **Configure LSEG credentials**:
   - Create `lseg-data.config.json` in the project root with your credentials.
   - Example format:
     {
    "logs": {
        "level": "info",
        "transports": {
            "console": {
                "enabled": false
            },
            "file": {
                "enabled": true,
                "name": "lseg-data-lib.log"
            }
        }
    },
    "sessions": {
        "default": "platform.ldp",
        "platform": {
            "ldp": {
                "app-key": "d619d*******************508f3",
                "username": "GE-A-***********",
                "password": "R*******78",
                "signon_control": true
            }
        }
    }
}

   - Replace the starred fields (`********`) with your actual LSEG username, password, and client ID.

5. **Run the server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   Or run in background:
   ```bash
   nohup uvicorn main:app --host 0.0.0.0 --port 8000 >> uvicorn.log 2>&1 &
   ```

6. **Access the application**:
   - Open `http://localhost:8000/input` in a browser.
   - Input currency pairs (e.g., `XAU=`, `JPY=`), submit, and view data at `http://localhost:8000/display`.
   - Use `http://localhost:8000/display_http` for HTTP polling if WebSocket fails (e.g., due to firewall).

## Notes
- Ensure port 8000 is open (`sudo ufw allow 8000` on Linux, or disable firewall on Windows).
- Logs are stored in `lseg-data-lib.log` with rotation (max 50MB).
- For remote access, check network and firewall settings.

## License
MIT License
