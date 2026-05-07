# 🌾 AgriTech — Plateforme de pilotage agricole

> Projet d'études Bachelor 2 — Sup de Vinci  
> Année 2025-2026

AgriTech est une application web conçue pour aider les acteurs agricoles à **surveiller leurs cultures, exploiter des données terrain et météo, et améliorer leur prise de décision**. L'application centralise les informations relatives aux parcelles, aux observations, aux alertes et aux conditions météorologiques en un seul tableau de bord clair et accessible.

Ce projet est réalisé dans le cadre d'une demande formulée par la Chambre d'Agriculture, dont l'objectif est de proposer un MVP fonctionnel répondant aux besoins de suivi des cultures et d'aide à la décision.

---

## 🚀 Fonctionnalités principales

- **Tableau de bord** : visualisation synthétique des indicateurs clés (surface exploitée, parcelles actives, alertes critiques, observations).
- **Gestion des parcelles** : ajout, consultation et association d'une culture (Blé, Maïs, Orge, Colza, Tournesol).
- **Observations terrain** : saisie de notes par parcelle (état, commentaire), consultation de l'historique, suppression.
- **Système d'alertes** : détection de situations à risque par niveaux (Faible, Modérée, Critique) avec filtres.
- **Météo agricole** : historique 7 jours, indicateurs agronomiques calculés (risque mildiou, humidité moyenne) et conseils du jour.
- **Carte interactive** : visualisation schématique des parcelles avec filtres par culture et recherche dynamique.
- **Authentification** : connexion utilisateur avec gestion des rôles.

---

## 🛠️ Stack technique

| Couche | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (vanilla) |
| **Backend** | Python 3, Flask, Flask-CORS |
| **Base de données** | SQLite |
| **Polices** | Inter, Plus Jakarta Sans (Google Fonts) |
| **Versioning** | Git / GitHub |

---

## 📁 Structure du projet

```
agri-tech-b2/
├── app.py                  # Serveur Flask + API REST
├── agritech.db             # Base de données SQLite (générée au lancement)
├── data.sql                # Données d'initialisation
├── MLD.sql                 # Modèle Logique de Données
├── requirements.txt        # Dépendances Python
├── static/
│   ├── style.css           # Styles centralisés
│   └── js/
│       └── main.js         # Logique JS partagée
├── templates/
│   ├── connexion.html      # Page de connexion
│   ├── index.html          # Tableau de bord
│   ├── parcelles.html      # Gestion des parcelles
│   ├── observations.html   # Notes terrain
│   ├── alertes.html        # Alertes & risques
│   ├── meteo.html          # Météo & prévisions
│   └── carte.html          # Carte interactive
└── README.md
```


## 🚀 Déploiement et Installation

### 🌐 Accès en ligne (Production)
L'application est déployée et accessible directement à cette adresse :  
👉 **[https://agri-tech-b2.vercel.app](https://agri-tech-b2.vercel.app)**

---

### 💻 Installation Locale (Développement)
Si vous souhaitez lancer le projet sur votre machine :

git clone https://github.com/Nightblue-star/agri-tech-b2.git
cd agri-tech-b2

python -m venv myenv

Activer l'environnement virtuel
Windows :
myenv\Scripts\activate

Mac/Linux :
source myenv/bin/activate

pip install -r requirements.txt

python app.py

Ouvrez l'adresse suivante : http://127.0.0.1:5000/

> La base de données SQLite et les données de test sont créées automatiquement au premier lancement.

---

## 🔐 Identifiants de test

Pour tester l'application sans créer de compte :

| Email | Mot de passe | Rôle |
|---|---|---|
| `test@agritech.fr` | `password123` | Agriculteur |

---

## 🚧 État du déploiement

Le projet est actuellement **fonctionnel en local** 

---

## 📚 Documentation complète

Une documentation détaillée est disponible et couvre :
- Le contexte et les objectifs du projet
- Le Modèle Conceptuel et Logique de Données (MCD / MLD)
- Le schéma d'architecture technique
- Les règles métier des alertes
- Les choix techniques justifiés
- L'organisation de l'équipe
- Les limites et perspectives d'évolution

---

## 👥 Équipe

Projet réalisé par les étudiants de Bachelor 2 — Sup de Vinci :

- **Adel** — Base de données (MCD, MLD, requêtes SQL)
- **Amine** — Backend Python / Flask (`app.py`) & responsive design & hebergement vercel & aide au front end
- **Clyfton** — Frontend (HTML, CSS, intégration des templates)
- **Ayoub** — CSS & contributions HTML

> L'historique des commits du dépôt Git reflète la répartition concrète du travail au sein de l'équipe.

---
