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
1. Clone this repository:
   ```bash
   git clone https://github.com/cristianku/opendbc-checksum-verifier.git
   cd opendbc-checksum-verifier
   ```

2. Open the Jupyter notebook:
   ```bash
   jupyter notebook "checking checksum.ipynb"
   ```

3. Run all cells to execute the checksum comparison tests.

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

## 📁 Files
- `checking checksum.ipynb` → main notebook for checksum validation  
- `logs/` *(optional)* → CAN log samples or extracted messages for testing  

---

## 🧠 Notes
- This project is for **development and verification** purposes only.  
- It does **not modify** any OpenPilot source files automatically.  
- Recommended for developers who work on **DBC or car porting** inside OpenPilot.

---

## 📜 License
MIT License © 2025 Cristian Zantedeschi
