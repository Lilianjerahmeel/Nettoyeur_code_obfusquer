# Scenario 2 : Obfuscation mixte
# Techniques : Hex + variables _0x + dead code + code inutile

_0x1a = "48656c6c6f"
_0x2b = "576f726c64"
_0x3c = "636f6e6e6563746564"

_0xff = 0
_0xab = 9999
_0xcd = "inutile"

junk1 = 42 + 0
junk2 = "rien"
junk3 = True

result1 = bytes.fromhex(_0x1a).decode("utf-8")
result2 = bytes.fromhex(_0x2b).decode("utf-8")
result3 = bytes.fromhex(_0x3c).decode("utf-8")

print(result1 + " " + result2)
print("Statut :", result3)