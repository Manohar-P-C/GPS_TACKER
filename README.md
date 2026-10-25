# GPS Tracker 🚌

A real-time GPS tracking prototype built using ESP32, a NEO-6M GPS module, Python, and Leaflet. The system collects GPS coordinates from the ESP32, transmits them over Wi-Fi to a Python server, and displays the reported location on an interactive map.

## Overview

This project explores a low-cost approach to GPS-based college bus tracking. It uses a GPS module to obtain geographical coordinates and a web interface to visualize the latest reported location.

## Features

- GPS coordinate acquisition using NEO-6M
- ESP32-based GPS data processing
- Wi-Fi communication between ESP32 and laptop
- Python HTTP server for receiving GPS data
- Interactive map using Leaflet and OpenStreetMap
- Automatic location refresh on the webpage

## System Architecture

GPS Module → ESP32 → Wi-Fi Hotspot → Python HTTP Server → Leaflet Map

## Hardware Requirements

- ESP32 development board
- NEO-6M GPS module
- USB cable and suitable power source
- Laptop
- Wi-Fi hotspot

## Technology Stack

| Component | Technology |
|---|---|
| Microcontroller programming | MicroPython |
| GPS communication | UART |
| Backend server | Python |
| Frontend | HTML, CSS, JavaScript |
| Mapping | Leaflet |
| Map data | OpenStreetMap |
| Version control | Git and GitHub |

## GPS Wiring

| GPS Module | ESP32 |
|---|---|
| TX | GPIO16 |
| RX | GPIO17 |
| GND | GND |
| VCC | 3.3V, as tested with the current module |

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd GPS_TRACKER
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

### 2. Configure the ESP32

Install MicroPython on the ESP32 and configure the Wi-Fi hotspot credentials in `main.py`.

Ensure the laptop and ESP32 connect to the same network. Keep credentials private and never commit real passwords.

### 3. Start the Python server

```bash
python server.py
```

### 4. Open the web interface

Open the following address in your browser:

```text
http://127.0.0.1:8000/
```

The laptop must remain powered on with the Python server running to receive GPS updates.

## Current Limitations

- The current prototype tracks the latest reported GPS position.
- The ESP32 and laptop must be connected to the same reachable network.
- Map tiles require internet access.
- GPS accuracy depends on satellite visibility and environmental conditions.
- The Python server currently stores the latest location in memory.

## Future Improvements

- Display predefined bus routes
- Support multiple buses
- Add estimated arrival times
- Deploy the backend for remote access
- Improve connection recovery and GPS status reporting

## Project Status

Prototype in development.

## License

Choose a license before distributing or accepting contributions to this project.
