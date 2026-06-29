# BASIC-PANEL

A Flask-based game cheat panel application with KeyAuth integration, memory manipulation, and DLL injection capabilities.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Customization Guide](#customization-guide)
- [Building the Application](#building-the-application)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.10 or higher
- Windows OS (required for memory manipulation and DLL injection features)
- Visual Studio Build Tools (for compiling certain dependencies)
- KeyAuth account with an application set up

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/BASIC-PANEL.git
cd BASIC-PANEL
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### KeyAuth Setup

1. Go to [KeyAuth Dashboard](https://keyauth.win)
2. Create a new application or use an existing one
3. Get your credentials from the application settings:
   - Application Name
   - Owner ID
   - Application Secret
   - Version

4. Update `app.py` with your KeyAuth credentials:

```python
keyauthapp = api(
    name = "YOUR_APP_NAME",     # Replace with your Application Name
    ownerid = "YOUR_OWNER_ID",   # Replace with your Owner ID (10 characters)
    secret = "YOUR_SECRET",      # Replace with your Application Secret (64 characters)
    version = "1.0",           # Replace with your Application Version
    hash_to_check = getchecksum()
)
```

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
KEYAUTH_NAME=REGIX STORE
KEYAUTH_OWNERID=JjpGjXJhfE
KEYAUTH_SECRET=f1e3904593d857cc2af43b4f59a3e008286677b82f15aeb8bf6fa4ca278a6265
KEYAUTH_VERSION=1.0
FLASK_SECRET_KEY=your-secret-key-here
```

## Project Structure

```
BASIC-PANEL/
├── app.py                  # Main Flask application entry point
├── Memory.py               # Memory manipulation and pattern scanning functions
├── keyauth.py              # KeyAuth API integration
├── utils.py                # Utility functions (process checking, etc.)
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── homepage.html
│   ├── sniper.html
│   ├── extra.html
│   ├── settings.html
│   └── partials/
│       ├── console.jinja
│       ├── emulator.jinja
│       ├── extra.jinja
│       ├── headshot.jinja
│       ├── settings.jinja
│       ├── sniper.jinja
│       ├── status.jinja
│       └── tabs.jinja
├── static/                 # Static assets
│   ├── js/
│   │   ├── console.js
│   │   ├── emulator.js
│   │   ├── extra.js
│   │   ├── headshot.js
│   │   ├── homepage.js
│   │   ├── settings.js
│   │   ├── sniper.js
│   │   └── status.js
│   └── images/
│       └── logo.png
└── dlls/                   # DLL injection files
    └── wallhack.dll
```

## Customization Guide

### Step 1: Update Application Name

In `app.py`, change the application name on line 19:

```python
keyauthapp = api(
    name = "Your Custom Name",  # Change this to your application name
    ...
)
```

### Step 2: Configure DLL Injection

The application uses DLLs for cheat functionality. To customize:

1. Place your custom DLLs in the `dlls/` folder
2. Update the injection paths in `app.py`:

```python
# For Chams Menu injection
inject(pid, Memory.get_resource_path('dlls/YOUR_DLL_NAME.dll'))

# For Chams 3D injection
inject(pid, Memory.get_resource_path('dlls/wallhack.dll'))
```

### Step 3: Modify Memory Patterns

Memory patterns are defined in `Memory.py`. To add or modify cheat patterns:

```python
# Example pattern in Memory.py
AIMBOT_PATTERN = "FF FF 00 00 ..."  # Your custom AOB pattern
DRAG_PATTERN = "00 00 00 00 ..."   # Your custom pattern
```

### Step 4: Add New Cheat Features

Create new endpoints in `app.py`:

```python
@app.post('/your-new-feature-on')
def yourFeatureOn():
    # Add your feature logic here
    return jsonify(status=200)
```

### Step 5: Update Frontend Templates

1. Edit HTML templates in `/templates/` to customize the UI
2. Add new styles to `/static/js/` JavaScript files
3. Update `base.html` for global CSS/JS includes

### Step 6: Configure Server Settings

In `app.py`, modify the Flask server configuration:

```python
app.run(debug=False, host='0.0.0.0', port=4070, threaded=True)
```

Change `port=4070` to your desired port number.

### Step 7: Customize Process Names

The application targets `HD-Player.exe` by default. To change the target process:

1. In `Memory.py`, update process names:
```python
process_name = "YourGame.exe"  # Replace HD-Player.exe
```

2. In `app.py`, update process checks:
```python
Memory.get_process("YourGame.exe")
```

3. In `utils.py`, update process manager targets:
```python
utils.check_process("YourProcess.exe")
```

## Building the Application

### Build Executable with PyInstaller

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the application
pyinstaller --onefile --windowed app.py
```

### Build with Custom Icon

```bash
pyinstaller --onefile --windowed --icon=logo.ico app.py
```

### Build Options Explained

| Option | Description |
|--------|-------------|
| `--onefile` | Bundles everything into a single executable |
| `--windowed` | Runs without console window (GUI only) |
| `--icon=ICON` | Sets the application icon |
| `--add-data` | Includes additional files (e.g., DLLs, templates) |

### Including DLLs in Build

```bash
pyinstaller --onefile --windowed --add-data "dlls;dlls" app.py
```

## Running the Application

### Development Mode

```bash
# Activate virtual environment first
python app.py
```

The server will start at `http://localhost:4070`

### Access Points

- Homepage: `http://localhost:4070/`
- Dashboard: `http://localhost:4070/dashboard`
- Sniper Panel: `http://localhost:4070/sniper-panel`
- Extra Panel: `http://localhost:4070/extra-panel`
- Settings: `http://localhost:4070/settings`

### Production Mode (Recommended)

Using Waitress WSGI server:

```bash
pip install waitress
```

Then modify the run command in `app.py`:

```python
from waitress import serve
serve(app, host='0.0.0.0', port=4070)
```

## Troubleshooting

### Common Issues

**1. Missing DLLs Error**
```
Solution: Ensure all required DLLs are in the dlls/ folder and paths are correct
```

**2. KeyAuth Authentication Failed**
```
Solution: Verify your credentials in app.py match the KeyAuth dashboard
```

**3. PyInstaller Build Fails**
```
Solution: Install Visual Studio Build Tools and ensure all dependencies are in requirements.txt
```

**4. Process Not Found**
```
Solution: Ensure HD-Player.exe is running or update to your target process name
```

### Debug Mode

To enable Flask debug mode, change in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=4070, threaded=True)
```

## Security Notice

⚠️ **DISCLAIMER**: This application contains memory manipulation and DLL injection capabilities. Use responsibly and only on systems you own or have explicit permission to modify. Unauthorized use may violate terms of service of games or applications.