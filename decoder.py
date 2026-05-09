"""
Module de décodage pour un outil de déobfuscation simple.

Ce module permet de :
- décoder du Base64
- décoder du Hexadécimal
- décoder un XOR simple avec une clé connue
"""

import base64

# ---------------------------------------------------
# Décodage Base64


def decode_base64(data):
    """
    Décode une chaîne Base64 en texte lisible.
    """

    try:
        decoded_bytes = base64.b64decode(data, validate=True)
        return decoded_bytes.decode("utf-8")

    except Exception:
        return None


# ---------------------------------------------------
# Décodage Hexadécimal


def decode_hex(data):
    """
    Convertit une chaîne hexadécimale en texte.
    """

    try:
        decoded_bytes = bytes.fromhex(data)
        return decoded_bytes.decode("utf-8")

    except Exception:
        return None
    

# ---------------------------------------------------
# Test du module


def test():

    # Base64
    b64 = "SGVsbG8="
    print("Base64 :", decode_base64(b64))

    # Hex
    hx = "48656c6c6f"
    print("Hex :", decode_hex(hx))
