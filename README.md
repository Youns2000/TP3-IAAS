# Azure IaaS TP - Application Web de Traducteur de Texte

## Description

L'application est une application web basée sur Flask, qui utilise le service Azure Translator Text pour traduire des textes d'une langue à une autre.

## Prérequis

- Python 3.7 ou supérieur
- Un environnement virtuel Python (recommandé)

## Installation

- Cloner le dépôt:

```bash
git clone https://github.com/Youns2000/TP3-IAAS.git
```

- Accédez au répertoire du projet:

```bash
cd TP3-IAAS
```

- (Optionnel) Créez et activez un nouvel environnement virtuel Python:

```bash
python3 -m venv env
source env/bin/activate  # Sur Unix ou MacOS
.\env\Scripts\activate   # Sur Windows
```

- Installez les dépendances du projet:

```bash
pip install -r requirements.txt
```

## Utilisation

- Exécutez le fichier app.py:

```bash
python app.py
```

- Accédez à http://127.0.0.1:5000 ou http://localhost:5000 dans votre navigateur.

Vous devriez maintenant voir l'interface de l'application et être en mesure de traduire du texte.
