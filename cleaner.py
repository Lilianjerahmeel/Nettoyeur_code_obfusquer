"""
Module de nettoyage et simplification de code obfusqué.

Ce module permet de :
- supprimer les lignes de code inutiles (dead code)
- renommer les variables suspectes (var_1, var_2, ...)
- reformater le code (indentation, espaces)
"""

import re


# ---------------------------------------------------
# Suppression du code inutile (dead code)

def remove_dead_code(code):
    """
    Supprime les lignes de code inutiles.

    Une ligne est considérée inutile si :
    - c'est une assignation à une variable qui n'est jamais relue
    - la variable assignée n'apparaît qu'une seule fois dans tout le code

    - code : chaîne de caractères représentant le script
    """

    lines = code.split('\n')
    cleaned_lines = []

    # On récupère toutes les variables assignées
    assign_pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=')

    # On compte combien de fois chaque nom apparaît dans le code
    name_counts = {}

    for line in lines:
        # On cherche tous les identifiants de la ligne
        tokens = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', line)
        for token in tokens:
            name_counts[token] = name_counts.get(token, 0) + 1

    for line in lines:
        match = assign_pattern.match(line)

        if match:
            var_name = match.group(1)

            # Si la variable n'apparaît qu'une seule fois (seulement l'assignation)
            # et que c'est une ligne simple sans appel de fonction
            if name_counts.get(var_name, 0) <= 1 and '(' not in line:
                # On ignore cette ligne (dead code)
                continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


# ---------------------------------------------------
# Renommage des variables suspectes

def rename_suspicious_variables(code):
    """
    Remplace les noms de variables peu lisibles par var_1, var_2, etc.

    Sont considérées comme suspectes :
    - les variables d'un seul caractère (a, b, x, z...)
    - les variables de deux caractères (x1, zz...)
    - les variables de type _0x... (style JavaScript obfusqué)

    - code : chaîne de caractères représentant le script
    """

    # Mots réservés Python à ne pas renommer
    python_keywords = {
        'if', 'else', 'elif', 'for', 'while', 'in', 'not', 'and', 'or',
        'is', 'return', 'def', 'class', 'import', 'from', 'as', 'try',
        'except', 'finally', 'with', 'pass', 'break', 'continue', 'True',
        'False', 'None', 'print', 'len', 'range', 'str', 'int', 'float',
        'list', 'dict', 'set', 'tuple', 'type', 'input', 'open', 'self'
    }

    # Détection des variables suspectes dans les assignations
    assign_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=')
    matches = assign_pattern.findall(code)

    suspicious = []

    for var in matches:
        if var in python_keywords:
            continue

        # Variable d'1 ou 2 caractères
        if len(var) <= 2 and var not in suspicious:
            suspicious.append(var)

        # Variable style _0x...
        elif re.match(r'^_0x[0-9a-fA-F]+$', var) and var not in suspicious:
            suspicious.append(var)

    # Remplacement dans le code
    counter = 1

    for var in suspicious:
        new_name = f"var_{counter}"
        counter += 1

        # Remplacement uniquement des mots entiers (pas dans d'autres mots)
        code = re.sub(r'\b' + re.escape(var) + r'\b', new_name, code)

    return code


# ---------------------------------------------------
# Reformatage du code

def reformat_code(code):
    """
    Reformate le code pour améliorer sa lisibilité.

    Actions effectuées :
    - suppression des lignes vides consécutives (plus de 2 d'affilée)
    - suppression des espaces en fin de ligne
    - correction de l'indentation via le module ast (si possible)
    """

    # Suppression des espaces en fin de ligne
    lines = [line.rstrip() for line in code.split('\n')]

    # Suppression des lignes vides consécutives
    cleaned_lines = []
    blank_count = 0

    for line in lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 1:
                cleaned_lines.append(line)
        else:
            blank_count = 0
            cleaned_lines.append(line)

    code = '\n'.join(cleaned_lines)

    return code


# ---------------------------------------------------
# Remplacement des chaînes encodées dans le code

def replace_encoded_strings(code, decoded_map):
    """
    Remplace les chaînes encodées par leur valeur décodée dans le code.

    - code        : le script à nettoyer
    - decoded_map : dictionnaire { chaîne_encodée : valeur_décodée }

    Exemple :
    decoded_map = { "SGVsbG8=" : "Hello" }
    """

    for encoded, decoded in decoded_map.items():
        # On cherche la chaîne entre guillemets simples ou doubles
        code = code.replace(f'"{encoded}"', f'"{decoded}"')
        code = code.replace(f"'{encoded}'", f'"{decoded}"')

    return code


# ---------------------------------------------------
# Nettoyage complet (pipeline principal)

def clean_code(code, decoded_map=None):
    """
    Lance le pipeline complet de nettoyage sur un script.

    Étapes :
    1. Remplacement des chaînes encodées (si decoded_map fourni)
    2. Renommage des variables suspectes
    3. Suppression du code inutile
    4. Reformatage

    - code        : script obfusqué en chaîne de caractères
    """

    # Étape 1 : remplacement des chaînes encodées
    if decoded_map:
        code = replace_encoded_strings(code, decoded_map)

    # Étape 2 : renommage des variables suspectes
    code = rename_suspicious_variables(code)

    # Étape 3 : suppression du dead code
    code = remove_dead_code(code)

    # Étape 4 : reformatage
    code = reformat_code(code)

    return code


# ---------------------------------------------------
# Test du module

def test():

    sample = '''
a = "SGVsbG8="
b = "48656c6c6f"
_0x12 = "test"
y = 999999

print(a)
print(b)
'''

    decoded_map = {
        "SGVsbG8=": "Hello",
        "48656c6c6f": "Hello"
    }

    print("=== Code original ===")
    print(sample)

    result = clean_code(sample, decoded_map)

    print("=== Code nettoyé ===")
    print(result)
