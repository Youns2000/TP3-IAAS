# Azure IaaS TP - Application Web de Traducteur de Texte

## Description

Ce projet contient une application web de traduction basée sur Flask. Il utilise le service Azure Translator Text pour traduire des textes d'une langue à une autre. Les utilisateurs peuvent entrer du texte ou télécharger des fichiers (PDF, TXT, DOCX) pour traduire dans une langue cible spécifiée.

## Prérequis

- Python 3.7 ou supérieur
- Un environnement virtuel Python (recommandé)
- Avoir une adresse e-mail @epita.fr valide pour l'authentification.

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

- Spécifiez que vous travaillez en local:
  Allez dans le fichier config.py et changez la valeur de la variable LOCAL à True.

```python
LOCAL = True
```

## Utilisation

- Exécutez le fichier app.py:

```bash
python app.py
```

- Accédez à http://127.0.0.1:5000 ou http://localhost:5000 dans votre navigateur.

Vous devriez maintenant voir l'interface de l'application et être en mesure de traduire du texte.
