# Genere_Polices_Assurance

=> Application web de géneration de polices d'assurances

## Description

Ce projet permet la gestion des clients, des polices d’assurance ainsi que des quittances. Il contient également une interface web sécurisée dédiées à l'administration des utilisateurs, des branches d'assurance, ainsi que des agences.

## Fonctionnalités

* Authentification des utilisateurs (Register/Login)

* Interface Admin
    -Gestion des Utilisateurs
    -Gestion des Branches d'assurance
    -Gestion des Agences ARO

* Interface User
    -Gestion des clients
    -Generation polices d’assurance
    -Historique polices d’assurance générée

* Autres fonctionnalités
    -Modification Profil Utilisateurs

* API REST (Postman) : [url de base API: http://127.0.0.1:8000/api]

    -Authentification des utilisateurs (Register/Login)
    -Gestion des Utilisateurs
    -Gestion des Branches d'assurance
    -Gestion des Agences ARO
    -Gestion des clients
    -Generation polices d’assurance
    -Gestion des quittances

*Documentation SWAGGER <http://127.0.0.1:8000/swagger/>

## Technologies utilisées

-Python 3.11+
-Django
-Django Rest Framework
-HTML/CSS/JS (jQuery)
-PostgreSQL (système de gestion de base de données relationnelle)

## Installation

1. Créer et activer un environnement virtuel :

   ```bash
   python -m venv env      
   source env/bin/activate  # Linux/macOS
   env\Scripts\activate     # Windows
   ```

2. Installer les dépendances :

   ```bash
   cd Genere_police
   pip install -r requirements.txt
   ```

3. Créer et configurer la base de données dans le fichier `.env`.

4. Appliquer les migrations :

   ```bash
   python manage.py migrate
   ```

5. Lancer le serveur :

   ```bash
   python manage.py runserver
   ```

## Contenue de .env

------------------------------

## Database

BDD_NAME = ..............
BDD_USER = ..............
BDD_PASSWORD = ..............
BDD_HOST = localhost
BDD_PORT = 5432

## SECRET_KEY

SECRET_KEY = ..............

## JWT_SECRET

JWT_SECRET=..............

## DEBUG

DEBUG = True (en développement)

------------------------------

## Structure du projet

Genere_police/
│
├── auth_app/            # Gestion des utilisateurs
├── agence_app/          # Gestion des agences
├── branch_app/          # Gestion des branches
├── client_app/          # Gestion des clients
├── police_app/          # Gestion des polices d’assurance
├── quittance_app/       # Gestion des quittances
├── Web_app/             # Vues frontend de l'application
├── static/              # Fichiers CSS, JS, images, fonts
├── templates/           # Templates HTML
├── Genere_police/       # Paramètres Django principaux
└── manage.py
