# 🧭 Bitcoin HD Wallet Derivation Explorer — Full BIP Hierarchy

This project implements a **multi-standard HD wallet derivation visualizer**  
that generates and exports the **entire BIP key tree** (BIP-44 / BIP-49 / BIP-84 / BIP-86)  
for a given mnemonic phrase — including extended keys and derived addresses.

> ⚠️ **For educational and cryptographic research only.**  
> Use this tool to learn and visualize hierarchical deterministic wallet paths —  
> never to access or expose private keys of live wallets.

---

## ⚙️ Features

✅ Derives full **BIP-44 / BIP-49 / BIP-84 / BIP-86** structures from a mnemonic  
✅ Displays each derivation level:  
- `m` — Master Key  
- `m/purpose'` — Purpose  
- `m/purpose'/0'` — Coin type (Bitcoin)  
- `m/purpose'/0'/0'` — Account  
- `m/purpose'/0'/0'/0/i` — External chain addresses  
✅ Generates both **xprv** and **xpub** for every level  
✅ Lists first `i = 0..N` derived addresses per BIP standard  
✅ Saves everything into a detailed text file for auditing  
✅ Built on the **bip_utils** cryptography library  

---

## 📂 File Structure

| File | Description |
|------|-------------|
| `bip_hd_explorer.py` | Main derivation script |
| `pelna_struktura_z_pelna_sciezka.txt` | Output file with full BIP hierarchy |
| `README.md` | Documentation (this file) |

---

## 🧮 How It Works

### 1️⃣ Generate Seed
The tool starts with a **BIP-39 mnemonic**:
```python
MNEMONIC = "action action action action action action action action action action action action"
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
2️⃣ Derive Master Key

From the seed, a Slip-10 Secp256k1 master key is created:

xprv (m)
xpub (m)

3️⃣ Iterate Through Standards

The script loops through multiple standards using a unified map:

BIP_MAP = {
    "BIP44": (Bip44, Bip44Coins.BITCOIN, "Legacy P2PKH"),
    "BIP49": (Bip49, Bip49Coins.BITCOIN, "Nested SegWit P2SH"),
    "BIP84": (Bip84, Bip84Coins.BITCOIN, "Native SegWit P2WPKH"),
    "BIP86": (Bip86, Bip86Coins.BITCOIN, "Taproot P2TR")
}


Each BIP defines its purpose field (44', 49', 84', 86') and derives:

m / purpose' / 0' / 0' / 0 / i


for i = 0 … MAX_INDEX-1.

4️⃣ Export Full Structure

All extended keys and derived addresses are written to:

pelna_struktura_z_pelna_sciezka.txt


Example output:

################## BIP84 - Native SegWit P2WPKH ##################

=== Purpose level (m/84') ===
xprv: xprv9uHRZZhk6KA...
xpub: xpub661MyMwAqRbc...

=== Coin level (m/84'/0') ===
xprv: xprv9wTYmMFsQ4b...
xpub: xpub68Gmy5Edvgib...

=== Account level (m/84'/0'/0') ===
xprv: xprv9zRjXZz4Kwx...
xpub: xpub6B8MmqSFeqUX...

=== Addresses m/84'/0'/0'/0/i ===
[0] bc1q8k9c2z9r...
[1] bc1qj38vxkld...
[2] bc1qrthfnl9s...

⚙️ Configuration
Constant	Description	Default
MNEMONIC	BIP-39 mnemonic phrase	"action action action..."
MAX_INDEX	Number of derived addresses per chain	10
OUTPUT_FILE	Output file name	pelna_struktura_z_pelna_sciezka.txt
BIP_MAP	Mapping of BIP standards	BIP-44 / 49 / 84 / 86
🧠 Technical Components
Function	Purpose
full_structure_with_levels()	Generates full BIP structure and writes results
Bip39SeedGenerator	Converts mnemonic to seed bytes
Bip32Slip10Secp256k1	Creates master extended key from seed
Bip44 / Bip49 / Bip84 / Bip86	Implements derivation logic for each BIP
ToExtended()	Exports xprv/xpub format strings
ToAddress()	Generates valid Bitcoin address for each derivation
🧩 Example Usage
python3 bip_hd_explorer.py


🧾 Console Output:

✅ Zapisano pełną strukturę wszystkich poziomów i BIP-ów do pliku: pelna_struktura_z_pelna_sciezka.txt

⚖️ Ethical Disclaimer

This script is designed for educational cryptography, wallet auditing, and key-derivation visualization.
It must never be used to access or regenerate someone else’s wallet.

Safe use cases:

Study HD derivation logic

Verify BIP paths

Backup and audit your own wallet

Do not use it for:

Unauthorized wallet access

Mainnet key reconstruction

🪪 License

MIT License
© 2025 — Author: [ethicbrudhack]

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
