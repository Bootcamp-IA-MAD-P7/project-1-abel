# Taxi Meter 🚖

A taxi meter system solution implemented in Python.

## 🚀 Features

- Calculate fare based on time (€0.02/s stopped, €0.05/s moving)
- **Interactive web dashboard** with control buttons
- **Real-time invoice** showing stopped time, moving time and total fare
- **Command history log** with timestamps
- **Automatic logging** of all trips in `logs/taxi-register.log`
- Simple and lightweight

## 📦 Requirements

- Python 3.x
- Flask
- Jinja2
- datetime
- logging

## 🔧 Setup

```bash
# Clone and enter directory
git clone https://github.com/Bootcamp-IA-MAD-P7/project-1-abel.git
cd project-1-abel

# Create virtual environment
python -m venv .venv

# Activate it
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the taxi meter
python app.py
```

## 📊 Usage
1. Start the application using `python app.py`.
2. Open your web browser and navigate to `http://localhost:5000`.
3. Input the commands in the interface.

## 📂 Interface commands
- `start`: Start the taxi meter.
- `stop`: Stop the taxi meter and calculate the fare.
- `move: <distance>`: Simulate moving the taxi and calculate the fare.
- `finish`: Finish the current trip and reset the meter.
- `exit`: Exit the application.

---

![version](https://img.shields.io/badge/version-1.0.0-green.svg)

## 📌 Version History

| Version      | Date       | Status | Description             |
| ------------ | ---------- | ------ | ----------------------- |
| v0.0.1-alpha | 2026-05-07 | ✅     | Initial project setup   |
| v0.1.0       | 2026-05-10 | ✅     | Base code & system Logs |
| v1.0.0       | 2026-05-18 | ✅     | First stable release    |
