def psa_checksum(address: int, sig, d: bytearray) -> int:
  # Skip disabled checksums (prefix "0_")
  if sig.name.startswith("0_"):
    return 0

  if sig.name == "CHECKSUM_CONS_RVV_LVV2":
    # Extract SPEED_SETPOINT from byte 1
    speed_setpoint = d[1]
    # Calculate parity of each nibble
    msb_nibble = (speed_setpoint >> 4) & 0xF
    lsb_nibble = speed_setpoint & 0xF
    # Count bits (parity): 1 if odd number of 1s, 0 if even
    msb_parity = bin(msb_nibble).count('1') & 1
    lsb_parity = bin(lsb_nibble).count('1') & 1
    # Return 2-bit checksum: [msb_parity, lsb_parity]
    return (msb_parity << 1) | lsb_parity

  # --- SPECIAL CASE: 0x305 (STEERING_ALT) ---
  if address == 0x305:
    # "checksum" is just the upper nibble of byte 4
    return (d[4] >> 4) & 0xF

  # --- 0x3AD: this ECU always sends 0 in that field ---
  if address == 0x3AD:
    return 0
  
  chk_ini = {0x452: 0x4,
             0x38D: 0x7,
             0x42D: 0xC,
             0x2B6: 0xC, # 694 decimal - HS2_DYN1_MDD_ETAT_2B6 - override 0xC su ECU MDD 2018+)
             0x2F6: 0x8,  # 758 decimal - messagmessage ACC2
             }.get(address, 0xB)
  byte = sig.start // 8
  d[byte] &= 0x0F if sig.start % 8 >= 4 else 0xF0

  checksum = sum((b >> 4) + (b & 0xF) for b in d)
  return (chk_ini - checksum) & 0xF
