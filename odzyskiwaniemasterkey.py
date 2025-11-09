from bip_utils import (
    Bip39SeedGenerator,
    Bip32Slip10Secp256k1,
    Bip44, Bip44Coins,
    Bip49, Bip49Coins,
    Bip84, Bip84Coins,
    Bip86, Bip86Coins,
    Bip44Changes
)

MNEMONIC = "action action action action action action action action action action action action"
MAX_INDEX = 10
OUTPUT_FILE = "pelna_struktura_z_pelna_sciezka.txt"

# Mapowanie BIP → odpowiednie klasy i opisy
BIP_MAP = {
    "BIP44": (Bip44, Bip44Coins.BITCOIN, "Legacy P2PKH"),
    "BIP49": (Bip49, Bip49Coins.BITCOIN, "Nested SegWit P2SH"),
    "BIP84": (Bip84, Bip84Coins.BITCOIN, "Native SegWit P2WPKH"),
    "BIP86": (Bip86, Bip86Coins.BITCOIN, "Taproot P2TR"),
}

def full_structure_with_levels(mnemonic: str, max_index: int, output_file: str):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    master = Bip32Slip10Secp256k1.FromSeed(seed_bytes)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"=== MNEMONIC ===\n{mnemonic}\n\n")

        f.write("=== MASTER KEY (m) ===\n")
        f.write(f"xprv (m): {master.PrivateKey().ToExtended()}\n")
        f.write(f"xpub (m): {master.PublicKey().ToExtended()}\n\n")

        for bip_name, (bip_class, coin, desc) in BIP_MAP.items():
            f.write(f"\n\n################## {bip_name} - {desc} ##################\n")

            # m/purpose'
            purpose_idx = {
                "BIP44": 44,
                "BIP49": 49,
                "BIP84": 84,
                "BIP86": 86
            }[bip_name]
            purpose = master.ChildKey(purpose_idx + 0x80000000)
            f.write(f"\n=== Purpose level (m/{purpose_idx}') ===\n")
            f.write(f"xprv: {purpose.PrivateKey().ToExtended()}\n")
            f.write(f"xpub: {purpose.PublicKey().ToExtended()}\n")

            # m/purpose'/0'
            coin_node = purpose.ChildKey(0 + 0x80000000)
            f.write(f"\n=== Coin level (m/{purpose_idx}'/0') ===\n")
            f.write(f"xprv: {coin_node.PrivateKey().ToExtended()}\n")
            f.write(f"xpub: {coin_node.PublicKey().ToExtended()}\n")

            # m/purpose'/0'/0'
            account_node = coin_node.ChildKey(0 + 0x80000000)
            f.write(f"\n=== Account level (m/{purpose_idx}'/0'/0') ===\n")
            f.write(f"xprv: {account_node.PrivateKey().ToExtended()}\n")
            f.write(f"xpub: {account_node.PublicKey().ToExtended()}\n")

            # Przejście do adresów użytkownika
            bip = bip_class.FromSeed(seed_bytes, coin)
            change = bip.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)

            f.write(f"\n=== Adresy m/{purpose_idx}'/0'/0'/0/i, i = 0..{max_index-1} ===\n")
            for i in range(max_index):
                addr = change.AddressIndex(i)
                f.write(f"[{i}] {addr.PublicKey().ToAddress()}\n")

    print(f"✅ Zapisano pełną strukturę wszystkich poziomów i BIP-ów do pliku: {output_file}")

# Uruchomienie
full_structure_with_levels(MNEMONIC, MAX_INDEX, OUTPUT_FILE)
