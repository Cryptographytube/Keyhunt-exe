import base58
from termcolor import colored
from datetime import datetime

def wif_to_hex(wif):
    try:
        decoded = base58.b58decode(wif)
        return decoded.hex()
    except Exception as e:
        print(f"[CRYPTOGRAPHYTUBE] [Error] WIF decode failed: {e}")
        exit(1)

def highlight_difference(start, end):
    match_len = 0
    for i in range(min(len(start), len(end))):
        if start[i] == end[i]:
            match_len += 1
        else:
            break
    common = start[:match_len]
    diff_start = colored(start[match_len:], 'red')
    diff_end = colored(end[match_len:], 'red')
    return common + diff_start, common + diff_end

def hex_to_int(hex_str):
    return int(hex_str, 16)

def count_bits(num):
    return num.bit_length()

def main():
    print("==== CRYPTOGRAPHYTUBE WIF Range Decoder (Compress & Uncompress Supported) ====\n")

    wif_input = input("Enter WIF with missing characters (*): ").strip()

    wif_filled_1 = wif_input.replace('*', '1')
    wif_filled_z = wif_input.replace('*', 'z')

    if len(wif_filled_1) == 51:
        mode = "uncompressed"
    elif len(wif_filled_1) == 52:
        mode = "compressed"
    else:
        print("[CRYPTOGRAPHYTUBE] [Error] Invalid WIF length (should be 51 or 52 characters).")
        exit(1)

    print(f"\n[CRYPTOGRAPHYTUBE] Detected Mode: {mode.upper()}\n")

    print("[CRYPTOGRAPHYTUBE] Decoding WIF filled with '1'...")
    hex_1 = wif_to_hex(wif_filled_1)
    print(f"{wif_filled_1}")
    print(f"{hex_1}\n")

    print("[CRYPTOGRAPHYTUBE] Decoding WIF filled with 'z'...")
    hex_z = wif_to_hex(wif_filled_z)
    print(f"{wif_filled_z}")
    print(f"{hex_z}\n")

    if mode == "compressed":
        privkey_start = hex_1[2:-10]
        privkey_end = hex_z[2:-10]
    else:
        privkey_start = hex_1[2:-8]
        privkey_end = hex_z[2:-8]

    print("[CRYPTOGRAPHYTUBE] Calculated Private Key Range:\n")
    diff_start, diff_end = highlight_difference(privkey_start, privkey_end)
    print(f"from: {diff_start}")
    print(f"to:   {diff_end}")

    int_start = hex_to_int(privkey_start)
    int_end = hex_to_int(privkey_end)
    combinations = int_end - int_start + 1
    bit_range = count_bits(combinations - 1) if combinations > 1 else 0

    print(f"\n[CRYPTOGRAPHYTUBE] Total Combinations: {combinations}")
    print(f"[CRYPTOGRAPHYTUBE] Bit Range: {bit_range} bits")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CRYPTOGRAPHYTUBE_{now}.txt"

    with open(filename, 'w') as f:
        f.write("==== CRYPTOGRAPHYTUBE WIF Range Decoder ====\n")
        f.write(f"Input WIF: {wif_input}\n")
        f.write(f"Mode: {mode.upper()}\n\n")
        f.write(f"WIF with '1': {wif_filled_1}\nHex: {hex_1}\n\n")
        f.write(f"WIF with 'z': {wif_filled_z}\nHex: {hex_z}\n\n")
        f.write(f"Private Key Start: {privkey_start}\n")
        f.write(f"Private Key End:   {privkey_end}\n\n")
        f.write(f"Total Combinations: {combinations}\n")
        f.write(f"Bit Range: {bit_range} bits\n")

    print(f"\n[CRYPTOGRAPHYTUBE] Result saved to: {filename}")

if __name__ == "__main__":
    main()
