# Windows Registry Monitor

A Python-based Windows Registry Change Monitoring System that detects
startup persistence techniques and security policy modifications
using baseline comparison and continuous monitoring.

This project is designed for cybersecurity learning and malware
persistence detection scenarios.

---

## Features

- Baseline creation of critical Windows Registry keys
- Detection of **new**, **modified**, and **deleted** registry values
- Monitors startup persistence locations:
  - Run
  - RunOnce
- Monitors Windows security policies:
  - Windows Defender policy keys
- Continuous monitoring with periodic checks
- Logs all detected changes with timestamps

---

## Registry Paths Monitored

- `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- `HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce`
- `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`
- `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce`
- `HKLM\Software\Policies\Microsoft\Windows Defender`

---

## Project Structure
windows-registry-monitor/
│
├── create_baseline.py # Creates initial registry baseline
├── compare_registry.py # Compares current state with baseline
├── baseline.json # Stored registry baseline
├── registry_changes.log # Logged registry changes
│
├── screenshots/ # Screenshots for report/demo
├── reports/ # Project report / PPT
│
└── README.md

---

## How to Run

### 1. Create Baseline
```bash
python create_baseline.py

