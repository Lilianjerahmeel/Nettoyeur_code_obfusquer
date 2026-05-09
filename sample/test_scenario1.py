# Scenario 1 : Obfuscation simple
# Techniques : Base64 + variables suspectes + dead code

import base64

a = "SGVsbG8gV29ybGQh"
b = "dXNlcm5hbWU="
c = "cGFzc3dvcmQxMjM="

x = 999
y = 12345
z = 0

decoded = base64.b64decode(a).decode("utf-8")
u = base64.b64decode(b).decode("utf-8")
p = base64.b64decode(c).decode("utf-8")

print(decoded)
print("Connexion avec :", u)
print("Mot de passe   :", p)