# Genere Polices Assurance

Application web de génération de polices d'assurance.

## Description

Ce projet permet de gérer les clients, les polices d'assurance et les quittances. Il propose :

- une **interface web sécurisée** pour l'administration (utilisateurs, branches d'assurance, agences) et pour les agents (clients, polices) ;
- une **API REST** documentée avec Swagger, utilisable avec Postman.

Les numéros de police, de compte client et de quittance sont générés automatiquement et sont uniques, même quand plusieurs polices sont créées en même temps.

## Fonctionnalités

### Authentification
- Inscription et connexion des utilisateurs
- Session sécurisée par un token JWT stocké dans un cookie `HttpOnly`
- Modification du profil utilisateur (nom, photo)

### Interface Admin
- Gestion des utilisateurs
- Gestion des branches d'assurance
- Gestion des agences

### Interface Utilisateur
- Gestion des clients
- Génération de polices d'assurance
- Historique des polices générées (statut mis à jour automatiquement : actif / expirée)

### API REST
Base de l'API : `http://127.0.0.1:8000/api`

- Authentification (inscription / connexion)
- Gestion des utilisateurs
- Gestion des branches d'assurance
- Gestion des agences
- Gestion des clients
- Génération des polices d'assurance
- Gestion des quittances

Documentation Swagger : <http://127.0.0.1:8000/swagger/>

## Technologies utilisées

- Python 3.11+
- Django
- Django REST Framework
- JWT (PyJWT)
- HTML / CSS / JavaScript (jQuery)
- PostgreSQL
- pytest et pytest-django (tests)

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/AnjaNyAina2003/Police_Assurance.git
   cd Police_Assurance/Genere_police
   ```

2. **Créer et activer un environnement virtuel**

   ```bash
   python -m venv env
   source env/bin/activate   # Linux / macOS
   env\Scripts\activate      # Windows
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Créer la base de données PostgreSQL**, puis le fichier `.env` (voir la section suivante).

5. **Appliquer les migrations**

   ```bash
   python manage.py migrate
   ```

6. **Créer le premier administrateur**

   ```bash
   python manage.py createsuperuser
   ```

   Les comptes créés depuis la page d'inscription ont le rôle `user`. Seul un compte créé avec `createsuperuser` obtient le rôle `admin`.

7. **Lancer le serveur**

   ```bash
   python manage.py runserver
   ```

   Garde le port `8000` : l'interface web appelle l'API à cette adresse.

## Configuration du fichier `.env`

Crée un fichier `.env` à côté de `manage.py` (modèle : `.env.example`). Ne le publie jamais sur GitHub.

```env
# Base de données
BDD_NAME=
BDD_USER=
BDD_PASSWORD=
BDD_HOST=localhost
BDD_PORT=5432

# Clés secrètes (valeurs longues et aléatoires, différentes l'une de l'autre)
SECRET_KEY=
JWT_SECRET=

# Mode debug (True en développement uniquement)
DEBUG=True
```

Pour générer une clé :

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## Tests

```bash
pytest
```

Le test vérifie que la génération simultanée de plusieurs polices produit toujours des numéros différents.

## Structure du projet

```
Genere_police/
│
├── auth_app/            # Utilisateurs et authentification
├── agence_app/          # Agences
├── branch_app/          # Branches d'assurance
├── client_app/          # Clients
├── police_app/          # Polices d'assurance (et tests)
├── quittance_app/       # Quittances
├── Web_app/             # Vues de l'interface web
├── static/              # CSS, JS, images, polices
├── templates/           # Templates HTML
├── Genere_police/       # Paramètres Django principaux
├── requirements.txt
└── manage.py
```
