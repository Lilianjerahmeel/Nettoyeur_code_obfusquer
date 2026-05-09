# 🔍 Nettoyeur de Code Obfusqué
---

## 📌 Description

Cet outil permet d'analyser un script Python obfusqué **sans l'exécuter**, d'en détecter les parties suspectes et de produire une version plus lisible et nettoyée. Il s'appuie uniquement sur l'analyse statique du code source.

---

## ✨ Fonctionnalités

- 🔎 **Détection** des chaînes encodées en Base64 et Hexadécimal
- 🔓 **Décodage** automatique des chaînes détectées
- 🏷️ **Renommage** des variables peu lisibles (`a`, `_0x12`, `zz`...)
- 🗑️ **Suppression** du code inutile (dead code)
- 🧹 **Reformatage** du code (indentation, espaces)
- 🖥️ **Interface graphique** intuitive développée avec Tkinter
- 💾 **Sauvegarde** du script nettoyé dans un dossier `output/`

---

## 🗂️ Structure du projet

```
obfuscation_cleaner/
│
├── main.py          # Point d'entrée — interface graphique Tkinter
├── detector.py      # Détection : Base64, Hex, variables suspectes
├── decoder.py       # Décodage : Base64 et Hexadécimal
├── cleaner.py       # Nettoyage : dead code, renommage, reformatage
│
├── samples/         # Scripts de test (voir avertissement ci-dessous)
│   ├── test_scenario1.py
│   ├── test_scenario2.py
│   └── test_scenario3.py
│
└── output/          # Scripts nettoyés (générés automatiquement)
```

---

## ⚠️ Avertissement sur les fichiers de test

> **Les fichiers présents dans le dossier `samples/` ne sont PAS des logiciels malveillants.**
>
> Il s'agit de scripts Python **artificiellement obfusqués**, créés uniquement à des fins **pédagogiques** pour tester les fonctionnalités de l'outil. Ils ne contiennent aucun code nuisible, aucun payload malveillant, et n'effectuent aucune action dangereuse. Ils simulent simplement différentes techniques d'obfuscation (Base64, Hexadécimal, variables renommées, dead code) sur des données fictives.

---

## 🚀 Installation et lancement

### Prérequis

- Python 3.8 ou supérieur
- Tkinter (inclus par défaut avec Python sur Windows et macOS)

Sur Linux, si Tkinter n'est pas installé :

```bash
sudo apt install python3-tk
```

### Lancer l'application

```bash
# Cloner le dépôt
git https://github.com/Lilianjerahmeel/Nettoyeur_code_obfusquer.git
cd Nettoyeur_code_obfusquer

# Lancer l'interface
python main.py
```

Aucune dépendance externe n'est requise. Toutes les bibliothèques utilisées (`re`, `base64`, `ast`, `tkinter`, `os`) font partie de la bibliothèque standard Python.

---

## 🖥️ Utilisation

1. Lancer `main.py`
2. Cliquer sur **"Choisir un fichier .py"** et sélectionner un script à analyser
3. Cliquer sur **"Nettoyer le code"**
4. Le code nettoyé s'affiche à droite, accompagné d'un rapport d'analyse
5. Le fichier nettoyé est automatiquement sauvegardé dans le dossier `output/`

---

## 🧩 Description des modules

### `detector.py`
Analyse le code source et détecte :
- Les chaînes encodées en **Base64** via regex + validation
- Les chaînes encodées en **Hexadécimal** via regex + validation
- Les **variables suspectes** : noms trop courts (`a`, `x1`) ou style JavaScript obfusqué (`_0x12`)

### `decoder.py`
Contient les fonctions de décodage :
- `decode_base64(data)` — décode une chaîne Base64 en texte UTF-8
- `decode_hex(data)` — convertit une chaîne hexadécimale en texte

### `cleaner.py`
Pipeline de nettoyage en 4 étapes :
1. Remplacement des chaînes encodées par leur valeur décodée
2. Renommage des variables suspectes en `var_1`, `var_2`...
3. Suppression des assignations inutiles (dead code)
4. Reformatage : suppression des espaces en fin de ligne, réduction des lignes vides consécutives

### `main.py`
Interface graphique Tkinter en deux colonnes :
- **Gauche** : fichier source original
- **Droite** : code nettoyé + rapport d'analyse (nombre de lignes supprimées, détections)

---

## 📊 Exemples de résultats

| Scénario | Technique | Lignes supprimées | Détections |
|---|---|---|---|
| Scénario 1 | Base64 simple | 4 | 3 chaînes Base64 |
| Scénario 2 | Hex + dead code | 8 | 3 chaînes Hex, 6 variables |
| Scénario 3 | Détection mixte | 9 | 3 Base64 + 2 Hex, 10 variables |

---

## ⚙️ Limites connues

- Le décodage **XOR** n'est pas pris en charge (nécessite une clé)
- Les obfuscations **multicouches** (Base64 d'un Hex) ne sont pas gérées
- L'outil est limité aux scripts **Python** uniquement
- L'analyse est purement **statique** : tout code dynamique échappe à la détection

---

## 🔮 Améliorations envisagées

- Ajout du décodage XOR avec saisie manuelle ou brute-force de la clé
- Analyse structurelle complète via le module `ast` (fonctions inutilisées, blocs morts)
- Extension à d'autres langages : JavaScript, PHP
- Gestion des obfuscations multicouches par pipeline récursif

---

## 👤 Auteur

**YANGUENDJI Jerahmeel Lilian**
Email : liyanguendji@gmail.com
linkedIn : linkedin.com/in/lilian-yanguendji
---

## 📄 Licence

Ce projet est développé à des fins **académiques et pédagogiques**.
Libre de réutilisation avec mention de l'auteur.
