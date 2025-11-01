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
- **Automatic checksum detection**: Finds all signals with "CHECKSUM" or "CRC" in the name from your DBC file
- **Multiple checksums support**: Handles messages with multiple checksum fields simultaneously
- **Batch verification**: Processes thousands of CAN messages from logs
- **Detailed statistics**: Shows success/failure rate for each checksum field
- **CSV export**: Generates reports with all messages and a separate file for failures only
- **Customizable**: Works with any car brand - just plug in your checksum function and DBC file

---

## 🚀 Usage

### Step 1: Export CAN logs from Cabana
1. Go to [connect.comma.ai](https://connect.comma.ai) and find your drive
2. Copy the route ID (e.g., `aa0ad8ba95ff270c|00000012--15c0b13b3a`)
3. Open [Cabana](https://cabana.comma.ai) and paste the route ID
4. Click **Export to CSV** to download the CAN log file
5. Save the CSV file in the `logs/` directory

### Step 2: Quick Start
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

### Batch Processing (Advanced)
For checking **all messages with checksums** in your DBC at once, you can use one of the specialized batch scripts:

#### 1. Messages Sent by Car (Original CAN Bus)
```bash
jupyter notebook "checking all checksums batch sent by car.ipynb"
```

This script analyzes **messages sent directly by the car** on the original CAN buses (0-3):
- Scans your entire DBC file for all messages containing checksum fields
- Searches for messages on buses 0, 1, 2, 3 (car's original CAN buses)
- Special handling for HS2_DAT_MDD_CMD_452 (0x452): forces bus 1 only
- Processes all checksum-enabled messages in one run
- Generates comprehensive statistics with success/failure rates
- Shows final aggregate summary with all messages analyzed

#### 2. Messages Sent by Panda (Forwarded by Device)
```bash
jupyter notebook "checking all checksums batch sent by PANDA.ipynb"
```

This script analyzes **messages forwarded by the Panda device** (buses >= 128):
- Searches for messages on buses 128, 129, 130 (Panda forwarded buses)
- Useful for verifying checksums on messages that Panda receives and retransmits
- Same comprehensive statistics and analysis as the car version
- Helps identify if checksum issues are related to message forwarding

**Configuration**: Only set `LOG_FILE` and `DBC_FILE` - both scripts find all messages automatically!

**Use Case**:
- Use **"sent by car"** to verify original car messages and checksum implementation
- Use **"sent by PANDA"** to verify messages forwarded by Panda device
- Compare both outputs to identify discrepancies between original and forwarded messages

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
├── checking checksum.ipynb                      # Single message checksum validation
├── checking all checksums batch.ipynb           # Batch processing for all messages (legacy)
├── checking all checksums batch sent by car.ipynb   # Batch: messages from car (bus 0-3)
├── checking all checksums batch sent by PANDA.ipynb # Batch: messages from Panda (bus >=128)
├── python/
│   └── psa_checksum.py                          # Checksum function (replace with yours!)
├── dbc/
│   └── your_car.dbc                             # Your DBC file
├── logs/
│   └── your_log.csv                             # CAN logs in CSV format (bus, addr, data, time)
└── output/
    ├── message_0xXXX_with_checksum.csv          # All messages with verification
    └── message_0xXXX_checksum_FAILS.csv         # Only failed checksums
```

### CSV Log Format
Your CAN log CSV must have these columns:
- `bus` - CAN bus number
  - **0-3**: Original car CAN buses (messages sent by car)
  - **128-130**: Panda forwarded buses (messages retransmitted by Panda device)
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
