# 🧮 opendbc-checksum-verifier

## Overview
This repository is designed to **verify and validate checksum functions** used in **opendbc car porting**.  
Its goal is to ensure that each message’s checksum logic in DBC files or OpenPilot ports behaves correctly and matches the expected OEM behavior.

The included Jupyter Notebook (`checking checksum.ipynb`) provides a controlled environment for inspecting, testing, and comparing checksum algorithms used in CAN message encoding/decoding.

---

## 🎯 Purpose
When porting a new car to OpenPilot, verifying the correctness of message checksums is critical.  
Incorrect checksum implementations may cause:
- CAN communication errors  
- EPS or ECU message rejection  
- LKA/LKAS failure to activate  

This tool helps developers confirm that checksum functions implemented in `opendbc` or `car/*/` code are correct before deploying.

---

## ⚙️ Features
- Load CAN messages and DBC definitions.  
- Compute checksums using OpenDBC logic.  
- Compare against expected checksums captured from real vehicle logs.  
- Identify mismatches and highlight possible implementation issues.  

---

## 🚀 Usage

### Quick Start
1. Clone this repository:
   ```bash
   git clone https://github.com/cristianku/opendbc-checksum-verifier.git
   cd opendbc-checksum-verifier
   ```

2. **Replace the checksum function** with your own implementation:
   - Edit `python/psa_checksum.py` (or create your own module)
   - Implement your car's checksum algorithm

3. **Configure the notebook** (`checking checksum.ipynb`):
   - Set `MESSAGE_ID` to the hex address of the message you want to check (e.g., `0x452`)
   - Set `DBC_FILE` to your DBC file path
   - Set `LOG_FILE` to your CAN log CSV file
   - Set `BUS` to the correct CAN bus number

4. **Run the notebook**:
   ```bash
   jupyter notebook "checking checksum.ipynb"
   ```
   The script will **automatically detect all signals** in your message that contain the word "CHECKSUM" or "CRC" and verify each one.

### How It Works
- The script reads your **DBC file** and automatically finds all signals with "CHECKSUM" or "CRC" in the name
- It compares the **extracted checksum** from real CAN messages against the **calculated checksum** using your function
- Outputs detailed statistics and CSV files with matches/mismatches

---

## 🧩 Dependencies
Make sure you have the following installed:
```bash
pip install jupyter pandas cantools numpy
```

If you are using OpenPilot’s environment:
```bash
source openpilot/.venv/bin/activate
```

---

## 📁 Project Structure
```
opendbc-checksum-verifier/
├── checking checksum.ipynb    # Main notebook for checksum validation
├── python/
│   └── psa_checksum.py        # Checksum function (replace with yours!)
├── dbc/
│   └── your_car.dbc           # Your DBC file
├── logs/
│   └── your_log.csv           # CAN logs in CSV format (bus, addr, data, time)
└── output/
    ├── message_0xXXX_with_checksum.csv      # All messages with verification
    └── message_0xXXX_checksum_FAILS.csv     # Only failed checksums
```

### CSV Log Format
Your CAN log CSV must have these columns:
- `bus` - CAN bus number (0, 1, 2, etc.)
- `addr` - Message address in hex format (e.g., `0x452`)
- `data` - Message data in hex format (e.g., `0x00000200`)
- `time` - Timestamp in seconds

---

## 🧠 Notes
- This project is for **development and verification** purposes only.  
- It does **not modify** any OpenPilot source files automatically.  
- Recommended for developers who work on **DBC or car porting** inside OpenPilot.

---

## 📜 License
MIT License © 2025 Cristian Zantedeschi
