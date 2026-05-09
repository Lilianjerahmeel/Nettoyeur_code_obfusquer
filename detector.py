"""
Module de détection des techniques simples d’obfuscation.

Ce module permet de :
- détecter Base64
- détecter Hexadécimal
- détecter des chaînes XOR suspectes
- détecter des noms de variables peu lisibles
"""

import base64
import re


# ---------------------------------------------------
# Détection Base64

def is_base64(data):
    """
    Vérifie si une chaîne ressemble à du Base64.
    """

    if not isinstance(data, str):
        return False

    data = data.strip()

    # Longueur minimale, base64 produit des chaines multiple de 4
    if len(data) % 4 != 0:
        return False

    # Vérification du format Base64
    pattern = r'^[A-Za-z0-9+/=]+$'

    if not re.fullmatch(pattern, data):
        return False

    try:
        decoded = base64.b64decode(data, validate=True)

        # Vérifie si le résultat est décodable en UTF-8
        decoded.decode("utf-8")

        return True

    except Exception:
        return False

# ---------------------------------------------------
# Détection Hexadécimale

def is_hex(data):
    """
    Vérifie si une chaîne est en format hexadécimal.
    """

    if not isinstance(data, str):
        return False

    data = data.strip()

    if len(data) == 0:
        return False

    # Longueur paire obligatoire
    if len(data) % 2 != 0:
        return False

    pattern = r'^[0-9a-fA-F]+$'

    return bool(re.fullmatch(pattern, data))

# ---------------------------------------------------
# Détection de variables suspectes

def detect_suspicious_variables(code):
    """
    Recherche des noms de variables peu lisibles.

    Exemple :
    a
    x1
    _0x12
    zz
    """

    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*='

    matches = re.findall(pattern, code)

    suspicious = []

    for var in matches:

        # Variables très courtes
        if len(var) <= 2:
            suspicious.append(var)

        # Variables type _0x...
        elif re.match(r'^_0x[0-9a-fA-F]+$', var):
            suspicious.append(var)

    return suspicious

# ---------------------------------------------------
# Recherche de chaînes Base64 dans un code

def find_base64_strings(code):
    """
    Recherche les chaînes Base64 potentielles.
    """

    pattern = r'["\']([A-Za-z0-9+/=]{8,})["\']'

    matches = re.findall(pattern, code)

    results = []

    for match in matches:
        if is_base64(match):
            results.append(match)

    return results

# ---------------------------------------------------
# Recherche de chaînes Hex dans un code

def find_hex_strings(code):
    """
    Recherche les chaînes hexadécimales potentielles.
    """

    pattern = r'["\']([0-9a-fA-F]{6,})["\']'

    matches = re.findall(pattern, code)

    results = []

    for match in matches:
        if is_hex(match):
            results.append(match)

    return results

# ---------------------------------------------------
# Analyse globale du script

 
def analyze_script(code):
    """
    Analyse générale du script.
    """
 
    report = {
 
        "base64_strings": find_base64_strings(code),
 
        "hex_strings": find_hex_strings(code),
 
        "suspicious_variables": detect_suspicious_variables(code),
 
    }
 
    return report
 

# ---------------------------------------------------
# Test rapide

def test():

    sample_code = '''

a = "SGVsbG8="
b = "48656c6c6f"
_0x12 = "test"

print(a)
'''

    result = analyze_script(sample_code)

    print("=== Rapport d’analyse ===")
    print()

    print("Chaînes Base64 détectées :")
    print(result["base64_strings"])

    print()

    print("Chaînes Hex détectées :")
    print(result["hex_strings"])

    print()

    print("Variables suspectes :")
    print(result["suspicious_variables"])
