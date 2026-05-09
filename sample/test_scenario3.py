# Scenario 3 : Obfuscation avancée
# Techniques : Base64 + Hex + variables suspectes + dead code

import base64



# --- Chaînes Base64 ---
a  = "aHR0cHM6Ly9leGFtcGxlLmNvbQ=="
b  = "YWRtaW4="
c  = "c2VjcmV0X2tleV8xMjM="

# --- Chaînes Hex ---
_0x10 = "636f6e6e656374696f6e5f6f6b"
_0x20 = "6572726f725f61757468"


# --- Dead code ---
z1   = 0
z2   = 99999
z3   = "unused_string"
z4   = False
z5   = 3.14
flag = 0

# --- Logique principale ---
url     = base64.b64decode(a).decode("utf-8")
user    = base64.b64decode(b).decode("utf-8")
key     = base64.b64decode(c).decode("utf-8")

ok_msg  = bytes.fromhex(_0x10).decode("utf-8")
err_msg = bytes.fromhex(_0x20).decode("utf-8")

print("URL     :", url)
print("User    :", user)
print("Key     :", key)
print("Status  :", ok_msg)